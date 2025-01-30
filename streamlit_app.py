import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import tempfile

# Streamlit App Title
st.title("Screaming Frog CSV Analyzer")

# File Uploader for CSV Export from Screaming Frog
uploaded_file = st.file_uploader("Upload Screaming Frog Exported CSV (Internal URLs)", type=["csv"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        csv_path = temp_file.name
    
    # Load CSV Data
    df = pd.read_csv(csv_path)

    st.subheader("Internal Pages Overview")
    st.dataframe(df.head(20))

    # Status Code Distribution
    if "Status Code" in df.columns:
        st.subheader("Status Code Distribution")
        status_counts = df["Status Code"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(status_counts.index.astype(str), status_counts.values)
        ax.set_xlabel("Status Code")
        ax.set_ylabel("Count")
        ax.set_title("Status Code Distribution")
        st.pyplot(fig)
    
    # Word Count Distribution
    if "Word Count" in df.columns:
        st.subheader("Word Count Distribution")
        fig, ax = plt.subplots()
        ax.hist(df['Word Count'].dropna(), bins=20, edgecolor='black')
        ax.set_xlabel("Word Count")
        ax.set_ylabel("Frequency")
        ax.set_title("Word Count Distribution")
        st.pyplot(fig)
    
    # Internal Linking Depth
    if "Crawl Depth" in df.columns:
        st.subheader("Crawl Depth Analysis")
        depth_counts = df['Crawl Depth'].value_counts().sort_index()
        fig, ax = plt.subplots()
        ax.bar(depth_counts.index.astype(str), depth_counts.values)
        ax.set_xlabel("Crawl Depth")
        ax.set_ylabel("Count of URLs")
        ax.set_title("Crawl Depth Distribution")
        st.pyplot(fig)
    
    st.success("CSV Data Processed Successfully!")
else:
    st.write("Upload a Screaming Frog export CSV file to begin analysis.")
