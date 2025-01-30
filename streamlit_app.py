import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import tempfile

# Streamlit App Title
st.title("Matt's Frog Silencer")

# File Uploader for CSV Export from Screaming Frog
uploaded_file = st.file_uploader("Upload Screaming Frog Exported CSV (Internal URLs)", type=["csv"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        csv_path = temp_file.name
    
    # Load CSV Data
    df = pd.read_csv(csv_path)

    # Sidebar Filters
    st.sidebar.header("Filters")
    status_filter = st.sidebar.multiselect("Filter by Status Code", df["Status Code"].unique()) if "Status Code" in df.columns else []
    min_word_count, max_word_count = st.sidebar.slider("Filter by Word Count Range", int(df["Word Count"].min()), int(df["Word Count"].max()), (int(df["Word Count"].min()), int(df["Word Count"].max()))) if "Word Count" in df.columns else (0, 0)
    max_crawl_depth = st.sidebar.slider("Filter by Maximum Crawl Depth", int(df["Crawl Depth"].min()), int(df["Crawl Depth"].max()), int(df["Crawl Depth"].max())) if "Crawl Depth" in df.columns else 0
    
    # Apply Filters
    if status_filter:
        df = df[df["Status Code"].isin(status_filter)]
    if "Word Count" in df.columns:
        df = df[(df["Word Count"] >= min_word_count) & (df["Word Count"] <= max_word_count)]
    if "Crawl Depth" in df.columns:
        df = df[df["Crawl Depth"] <= max_crawl_depth]
    
    st.subheader("Filtered Internal Pages Overview")
    st.dataframe(df)

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
