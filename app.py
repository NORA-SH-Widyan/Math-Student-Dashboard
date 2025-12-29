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
    # clean column names
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
st.header("🔹 Section 1: Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Number of Students", df["student_id"].nunique() if "student_id" in df.columns else "N/A")

with col2:
    st.metric("Number of Questions", df["question_id"].nunique() if "question_id" in df.columns else "N/A")

with col3:
    st.metric("Average Accuracy", round(df["student_accuracy"].mean(), 3))

st.divider()

# =========================
# SECTION 2: Answer Analysis
# =========================
st.header("🔹 Section 2: Answer Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribution of Type of Answer")
    answer_counts = df["type_of_answer"].value_counts().sort_index()
    st.bar_chart(answer_counts)

with col2:
    st.subheader("Accuracy by Question Level")
    if "question_level" in df.columns:
        level_acc = df.groupby("question_level")["student_accuracy"].mean()
        st.bar_chart(level_acc)

st.divider()

# =========================
# SECTION 3: Difficulty Impact
# =========================
st.header("🔹 Section 3: Difficulty Impact")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Question Difficulty Distribution")
    fig, ax = plt.subplots()
    ax.hist(df["question_difficulty"], bins=20)
    ax.set_xlabel("Question Difficulty")
    ax.set_ylabel("Count")
    st.pyplot(fig)

with col2:
    st.subheader("Question Difficulty vs Accuracy")
    fig, ax = plt.subplots()
    ax.scatter(
        df["question_difficulty"],
        df["student_accuracy"],
        alpha=0.5
    )
    ax.set_xlabel("Question Difficulty")
    ax.set_ylabel("Student Accuracy")
    st.pyplot(fig)

st.divider()

# =========================
# SECTION 4: Topic Analysis
# =========================
st.header("🔹 Section 5: Topic Analysis")

top_topics = (
    df.groupby("topic")["student_accuracy"]
    .mean()
    .sort_values(ascending=False)
)

st.subheader("Average Accuracy by Topic")
st.bar_chart(top_topics)

# =========================
# SECTION 5: Key Insights
# =========================
st.header("🔹 Key Insights")

st.markdown("""
- Student accuracy decreases as question difficulty increases.
- Advanced questions tend to include longer and more complex keywords.
- Performance varies significantly across different mathematical topics.
- Text-based features provide useful signals for modeling student performance.
""")




#Boxplot
#Final Grade vs Type of Answer
if "G3" in df.columns:
    st.subheader("Final Grade by Type of Answer")
    fig, ax = plt.subplots()
    df.boxplot(column="G3", by="Type of Answer", ax=ax)
    ax.set_title("")
    ax.set_xlabel("Type of Answer")
    ax.set_ylabel("Final Grade")
    st.pyplot(fig)









# =========================
# Footer
# =========================
st.caption("Dashboard created using Streamlit • Math Education Dataset")
