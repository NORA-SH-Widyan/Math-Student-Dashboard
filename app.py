import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Math Students Performance Dashboard",
    layout="wide"
)

st.title("📊 Math Students Performance Dashboard")
st.markdown("Interactive exploratory analysis of students performance data.")

# =========================
# Load data
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "MathEdataset_dashboard.csv",
        sep=";",
        encoding="latin1",
        on_bad_lines="skip"
    )
    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

df = load_data()

# =========================
# SECTION 1: Overview
# =========================
st.header("🔹 Section 1: Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Number of Students",
        df["student_id"].nunique() if "student_id" in df.columns else "N/A"
    )

with col2:
    st.metric(
        "Number of Questions",
        df["question_id"].nunique() if "question_id" in df.columns else "N/A"
    )

with col3:
    st.metric(
        "Average Student Accuracy",
        round(df["student_accuracy"].mean(), 3)
    )

st.divider()

# =========================
# SECTION 2: Answer Analysis
# =========================
st.header("🔹 Section 2: Answer Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribution of Answer Types")
    answer_counts = df["type_of_answer"].value_counts().sort_index()
    st.bar_chart(answer_counts)

with col2:
    st.subheader("Average Accuracy by Question Level")
    if "question_level" in df.columns:
        level_acc = df.groupby("question_level")["student_accuracy"].mean()
        st.bar_chart(level_acc)

st.divider()

# =========================
# SECTION 3: Difficulty & Topic Overview
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Topics in the Dataset")
    if "topic" in df.columns:
        top_topics = df["topic"].value_counts().head(10)
        st.bar_chart(top_topics)
    else:
        st.info("Topic column not available.")

with col2:
    st.subheader("Question Difficulty Distribution")
    fig, ax = plt.subplots()
    ax.hist(df["question_difficulty"], bins=20)
    ax.set_xlabel("Question Difficulty")
    ax.set_ylabel("Count")
    st.pyplot(fig)


st.divider()

# =========================
# SECTION 4: Topic Performance
# =========================
st.header("🔹 Section 4: Topic Performance Analysis")

st.subheader("Average Student Accuracy by Topic")

topic_accuracy = (
    df.groupby("topic")["student_accuracy"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(topic_accuracy)

st.divider()

# =========================
# SECTION 5: Feature Exploration
# =========================
st.header("🔹 Section 5: Feature vs Student Accuracy")

# Select numeric features only
numeric_features = df.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

# Remove target variable
if "student_accuracy" in numeric_features:
    numeric_features.remove("student_accuracy")

if len(numeric_features) == 0:
    st.warning("No numeric features available for comparison.")
else:
    feature = st.selectbox(
        "Select a numeric feature:",
        numeric_features
    )

    fig, ax = plt.subplots()
    ax.scatter(
        df[feature],
        df["student_accuracy"],
        alpha=0.5
    )
    ax.set_xlabel(feature)
    ax.set_ylabel("Student Accuracy")
    ax.set_title(f"{feature} vs Student Accuracy")
    st.pyplot(fig)

st.divider()

# =========================
# SECTION 6: Key Insights
# =========================
st.header("🔹 Section 6: Key Insights")

st.markdown("""
- Student accuracy tends to decrease as question difficulty increases.
- Performance varies significantly across different mathematical topics.
- Certain topics show consistently higher student accuracy.
- Engineered numeric features provide useful signals for analyzing performance.
""")

# =========================
# Footer
# =========================
st.caption("Dashboard created using Streamlit • Math Education Dataset")
