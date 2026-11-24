import pandas as pd
import re
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR, "dataset", "passwords.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "model")

MODEL_PATH = os.path.join(
    MODEL_DIR, "password_model.pkl"
)


def extract_features(password):

    return {
        "length": len(password),
        "lowercase": int(bool(re.search(r"[a-z]", password))),
        "uppercase": int(bool(re.search(r"[A-Z]", password))),
        "digits": sum(c.isdigit() for c in password),
        "special": sum(not c.isalnum() for c in password),
        "unique_chars": len(set(password)),
        "repeated_chars": len(password) - len(set(password)),
        "has_sequence": int(
            any(
                seq in password.lower()
                for seq in ["123", "abc", "qwerty", "asdf"]
            )
        )
    }


def load_dataset():

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            "Dataset not found: dataset/passwords.csv"
        )

    df = pd.read_csv(DATASET_PATH)

    if not {"password", "strength"}.issubset(df.columns):
        raise ValueError(
            "Dataset must contain password and strength columns."
        )

    df = df.dropna(subset=["password", "strength"])

    X = pd.DataFrame(
        [extract_features(str(p)) for p in df["password"]]
    )

    y = df["strength"].astype(str)

    if y.nunique() < 2:
        raise ValueError(
            "Dataset must contain at least two strength classes."
        )

    return X, y


def train_model():

    X, y = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("MODEL TRAINING COMPLETED")
    print("-------------------------")
    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print("Model saved successfully!")

    return model


def get_model():

    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    return train_model()


def predict_strength(password):

    model = get_model()

    features = pd.DataFrame(
        [extract_features(password)]
    )

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    confidence = max(probabilities) * 100

    return {
        "prediction": str(prediction),
        "confidence": round(float(confidence), 2)
    }


if __name__ == "__main__":
    train_model()