import string
import math
import re

COMMON_PASSWORDS = {
    "123456", "123456789", "12345678",
    "password", "password123", "qwerty",
    "qwerty123", "admin", "admin123",
    "abc123", "111111", "123123",
    "iloveyou", "welcome", "letmein",
    "monkey", "dragon", "football",
    "1234567890", "000000", "passw0rd"
}

SEQUENCES = [
    "123", "234", "345", "456", "567",
    "678", "789", "890",
    "abc", "bcd", "cde", "def",
    "xyz", "qwerty", "asdf", "zxcv",
    "987", "876", "765", "654",
    "cba", "fed"
]


def check_patterns(password):
    lower_password = password.lower()

    repeated = bool(
        re.search(r"(.)\1{2,}", password)
    )

    sequential = any(
        sequence in lower_password
        for sequence in SEQUENCES
    )

    return {
        "repeated": repeated,
        "sequential": sequential
    }


def calculate_entropy(password):
    if not password:
        return 0

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(c in string.punctuation for c in password):
        charset += 32

    if any(c.isspace() for c in password):
        charset += 1

    if charset == 0:
        return 0

    return len(password) * math.log2(charset)


def calculate_crack_time(entropy):
    if entropy <= 0:
        return "Unknown"

    guesses_per_second = 1_000_000_000

    seconds = (
        (2 ** min(entropy, 1023))
        / (2 * guesses_per_second)
    )

    if seconds < 1:
        return "Less than a second"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds / 86400:.1f} days"
    elif seconds < 31536000 * 1000:
        return f"{seconds / 31536000:.1f} years"
    else:
        return "Over 1000 years"


def analyze_password(password):

    score = 0
    recommendations = []

    checks = {
        "At least 8 characters": len(password) >= 8,
        "At least 12 characters": len(password) >= 12,
        "Uppercase letters": any(c.isupper() for c in password),
        "Lowercase letters": any(c.islower() for c in password),
        "Numbers": any(c.isdigit() for c in password),
        "Special characters": any(
            c in string.punctuation for c in password
        )
    }

    for description, passed in checks.items():
        if passed:
            score += 1
        else:
            recommendations.append(
                f"Improve: {description}"
            )

    is_common = password.lower() in COMMON_PASSWORDS

    patterns = check_patterns(password)

    if is_common:
        recommendations.append(
            "Avoid commonly used passwords."
        )

    if patterns["repeated"]:
        recommendations.append(
            "Avoid repeating the same character multiple times."
        )

    if patterns["sequential"]:
        recommendations.append(
            "Avoid sequential letters or numbers."
        )

    if is_common:
        status = "Weak"
    elif score <= 2:
        status = "Weak"
    elif score <= 4:
        status = "Medium"
    else:
        status = "Strong"

    entropy = calculate_entropy(password)

    return {
        "score": score,
        "status": status,
        "length": len(password),
        "is_common": is_common,
        "patterns": patterns,
        "entropy": round(entropy, 2),
        "crack_time": calculate_crack_time(entropy),
        "checks": checks,
        "recommendations": recommendations
    }