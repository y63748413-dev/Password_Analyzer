import streamlit as st

from analyzer import analyze_password
from ai_model import predict_strength


# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Password Analyzer",
    page_icon="🔐",
    layout="wide"
)


# CUSTOM CSS
st.markdown("""
<style>

.stApp {
    background-color: #0b1120;
    color: #e2e8f0;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #38bdf8;
}

.subtitle {
    color: #94a3b8;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: #172338;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #263650;
}

div[data-testid="stMetricValue"] {
    color: #38bdf8;
}

section[data-testid="stSidebar"] {
    background-color: #111c30;
}

</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown(
    '<div class="main-title">🔐 AI Password Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Advanced Password Security Assessment System'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# SIDEBAR
with st.sidebar:
    st.title("🔐 Password Security")
    st.write("Machine Learning Powered Analysis")

    st.divider()

    st.markdown("### Application Features")

    st.write("🔍 Password Strength Analysis")
    st.write("🤖 Random Forest Prediction")
    st.write("🛡️ Common Password Detection")
    st.write("🔎 Pattern Detection")
    st.write("📊 Entropy Analysis")
    st.write("⏱️ Crack Time Estimation")

    st.divider()

    st.caption("AI Password Analyzer | 2026")


# PASSWORD INPUT
st.header("🔑 Password Testing")

password = st.text_input(
    "Enter your password",
    type="password",
    placeholder="Enter a password to analyze...",
    help="Your password is analyzed locally by this application."
)

if not password:

    st.info(
        "Enter a password above to start the security assessment."
    )

    st.markdown("### Why use this application?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🤖 AI Analysis")
        st.write("Machine Learning based password classification.")

    with col2:
        st.markdown("### 🛡️ Security Checks")
        st.write("Detection of common and predictable passwords.")

    with col3:
        st.markdown("### 📊 Detailed Results")
        st.write("Security score, entropy and estimated crack time.")

else:

    # RULE-BASED ANALYSIS
    analysis = analyze_password(password)

    st.divider()
    st.header("📊 Security Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Security Score",
            f"{analysis['score']}/6"
        )

    with col2:
        st.metric(
            "Password Length",
            analysis["length"]
        )

    with col3:
        st.metric(
            "Security Status",
            analysis["status"]
        )

    with col4:
        st.metric(
            "Entropy",
            f"{analysis['entropy']} bits"
        )

    st.progress(analysis["score"] / 6)

    # PASSWORD REQUIREMENTS
    st.divider()
    st.header("📋 Password Requirements")

    left, right = st.columns(2)

    checks = list(analysis["checks"].items())

    for index, (name, passed) in enumerate(checks):

        target = left if index % 2 == 0 else right

        with target:
            if passed:
                st.success(f"✓ {name}")
            else:
                st.error(f"✗ {name}")

    # COMMON PASSWORD DETECTION
    st.divider()
    st.header("🛡️ Common Password Detection")

    if analysis["is_common"]:
        st.error(
            "Common password detected! "
            "This password is easy to guess."
        )
    else:
        st.success(
            "No match found in the local common password list."
        )

    # PATTERN DETECTION
    st.divider()
    st.header("🔎 Pattern Detection")

    pattern_col1, pattern_col2 = st.columns(2)

    with pattern_col1:
        if analysis["patterns"]["repeated"]:
            st.warning("Repeated characters detected.")
        else:
            st.success("No repeated character pattern detected.")

    with pattern_col2:
        if analysis["patterns"]["sequential"]:
            st.warning("Sequential pattern detected.")
        else:
            st.success("No known sequential pattern detected.")

    # MACHINE LEARNING
    st.divider()
    st.header("🤖 Artificial Intelligence Analysis")

    try:

        result = predict_strength(password)

        prediction = result["prediction"]
        confidence = result["confidence"]

        ai_col1, ai_col2 = st.columns(2)

        with ai_col1:
            st.metric(
                "Random Forest Prediction",
                prediction
            )

        with ai_col2:
            st.metric(
                "Model Confidence",
                f"{confidence:.2f}%"
            )

        st.progress(
            max(0.0, min(confidence / 100, 1.0))
        )

        st.caption(
            "Model confidence is not the probability that "
            "a password is actually secure."
        )

    except Exception as error:

        st.error(
            f"AI Model could not complete the prediction: {error}"
        )

    # CRACK TIME
    st.divider()
    st.header("⏱️ Crack Time Estimation")

    st.info(
        f"Estimated time: {analysis['crack_time']}"
    )

    st.caption(
        "Theoretical estimate using an assumed rate of "
        "1 billion guesses per second and half of the "
        "estimated search space. Real results can differ."
    )

    # RECOMMENDATIONS
    st.divider()
    st.header("💡 Security Recommendations")

    if analysis["recommendations"]:

        for recommendation in analysis["recommendations"]:
            st.warning("⚠️ " + recommendation)

    else:

        st.success(
            "No basic security issues were detected."
        )

    # FINAL ASSESSMENT
    st.divider()
    st.header("📝 Final Security Assessment")

    if analysis["is_common"] or analysis["status"] == "Weak":

        st.error(
            "Your password needs improvement. "
            "Choose a longer and less predictable password."
        )

    elif analysis["status"] == "Medium":

        st.warning(
            "Your password has moderate security. "
            "Consider improving its complexity and uniqueness."
        )

    else:

        st.success(
            "Your password meets the basic security criteria. "
            "Consider using a unique password for every account."
        )


# FOOTER
st.divider()

st.caption(
    "AI Password Analyzer | Educational Information Security Project"
)

st.caption(
    "Passwords are processed in application memory and are not "
    "intentionally stored by this application. "
    "Do not enter real personal passwords during testing."
)