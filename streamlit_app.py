import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("Screaming Frog Crawl Analyzer")

# File Uploader
uploaded_file = st.file_uploader("Upload Screaming Frog SQLite Database", type=["db", "sqlite"])

if uploaded_file:
    # Save uploaded file temporarily
    db_path = "uploaded_crawl.db"
    with open(db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
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
    status_counts = df['StatusCode'].value_counts()
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

st.write("Upload a Screaming Frog SQLite database to begin analysis.")
