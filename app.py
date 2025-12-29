import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Math Students Dashboard", layout="wide")

st.title("📊 Math Students Performance Dashboard")
st.success("App started successfully ✅")

@st.cache_data
def load_data():
    return pd.read_csv(
        "MathEdataset_dashboard.csv",
        sep=";",
        encoding="latin1",
        on_bad_lines="skip"
    )

df = load_data()

st.write("Dataset Preview")
st.dataframe(df.head())

#Bar Chart/ Type of Answer
st.subheader("Distribution of Type of Answer")
answer_counts = df["Type of Answer"].value_counts().sort_index()
st.bar_chart(answer_counts)

#Histogram:
#Student Accuracy (Numeric)
st.subheader("Student Accuracy Distribution")
fig, ax = plt.subplots()
ax.hist(df["student_accuracy"], bins=20)
ax.set_xlabel("Student Accuracy")
ax.set_ylabel("Count")
st.pyplot(fig)

#Question Difficulty
st.subheader("Question Difficulty Distribution")
fig, ax = plt.subplots()
ax.hist(df["question_difficulty"], bins=20)
ax.set_xlabel("Question Difficulty")
ax.set_ylabel("Count")
st.pyplot(fig)

#Question Level (Categorical)
st.subheader("Question Level Distribution")
level_counts = df["Question Level"].value_counts()
st.bar_chart(level_counts)

#Boxplot
#Keywords Word Count (Text → Numeric)
st.subheader("Keywords Word Count")
fig, ax = plt.subplots()
ax.boxplot(df["keywords_word_count"].dropna(), vert=False)
ax.set_xlabel("Word Count")
st.pyplot(fig)

#Boxplot: Final Grade vs Type of Answer
if "G3" in df.columns:
    st.subheader("Final Grade by Type of Answer")
    fig, ax = plt.subplots()
    df.boxplot(column="G3", by="Type of Answer", ax=ax)
    ax.set_title("")
    ax.set_xlabel("Type of Answer")
    ax.set_ylabel("Final Grade")
    st.pyplot(fig)



 















