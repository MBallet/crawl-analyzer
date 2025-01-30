import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

# Increase the max upload size to 1GB (adjust as needed)
os.makedirs(os.path.expanduser("~/.streamlit"), exist_ok=True)
with open(os.path.expanduser("~/.streamlit/config.toml"), "w") as f:
    f.write("[server]\nmaxUploadSize = 1000\n")

# Streamlit App Title
st.title("Screaming Frog Crawl Analyzer")

# File Uploader
uploaded_file = st.file_uploader("Upload Screaming Frog Crawl Data (.seospider)", type=["seospider"])

if uploaded_file:
    # Save uploaded file temporarily
    seospider_path = "uploaded_crawl.seospider"
    with open(seospider_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract the .seospider file (it's a ZIP archive)
    extract_path = "extracted_crawl"
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(seospider_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    # Find the SQLite file (.db) inside the extracted folder
    db_file = None
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if file.endswith(".db"):
                db_file = os.path.join(root, file)
                break

    if db_file:
        st.success(f"Extracted SQLite DB: {db_file}")

        # Connect to the extracted SQLite database
        conn = sqlite3.connect(db_file)

        # Show Available Tables
        st.subheader("Available Tables")
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
        st.write(tables)

        # Load Internal URLs Table
        query = "SELECT Address, StatusCode, Title1, WordCount, CrawlDepth FROM internal"
        df = pd.read_sql(query, conn)

        st.subheader("Internal Pages Overview")
        st.dataframe(df.head(20))

        # Status Code Distribution
        st.subheader("Status Code Distribution")
        status_counts = df["StatusCode"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(status_counts.index.astype(str), status_counts.values)
        ax.set_xlabel("Status Code")
        ax.set_ylabel("Count")
        ax.set_title("Status Code Distribution")
        st.pyplot(fig)

        # Word Count Distribution
        st.subheader("Word Count Distribution")
        fig, ax = plt.subplots()
        ax.hist(df['WordCount'].dropna(), bins=20, edgecolor='black')
        ax.set_xlabel("Word Count")
        ax.set_ylabel("Frequency")
        ax.set_title("Word Count Distribution")
        st.pyplot(fig)

        # Internal Linking Depth
        st.subheader("Crawl Depth Analysis")
        depth_counts = df['CrawlDepth'].value_counts().sort_index()
        fig, ax = plt.subplots()
        ax.bar(depth_counts.index.astype(str), depth_counts.values)
        ax.set_xlabel("Crawl Depth")
        ax.set_ylabel("Count of URLs")
        ax.set_title("Crawl Depth Distribution")
        st.pyplot(fig)

        # Close Connection
        conn.close()
    else:
        st.error("Could not find a SQLite database (.db) inside the uploaded .seospider file.")

st.write("Upload a Screaming Frog crawl data file (.seospider) to begin analysis.")
