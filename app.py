import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Math Students Dashboard", layout="wide")

st.title("📊 Math Students Performance Dashboard")
st.success("App started successfully ✅")

# Load data
df = pd.read_csv(
    "MathEdataset_dashboard.csv",
    sep=";",
    encoding="latin1",
    on_bad_lines="skip"
)

st.write("Dataset Preview")
st.dataframe(df.head())
