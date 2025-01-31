import streamlit as st
import pandas as pd
import plotly.express as px
import os
import tempfile

# Streamlit App Title with Image
st.title("Screaming Frog CSV Analyzer")
st.image("Frog - open.png", width=400) 

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
    min_unique_inlinks, max_unique_inlinks = st.sidebar.slider("Filter by Unique Inlinks Range", int(df["Unique Inlinks"].min()), int(df["Unique Inlinks"].max()), (int(df["Unique Inlinks"].min()), int(df["Unique Inlinks"].max()))) if "Unique Inlinks" in df.columns else (0, 0)
    
    # Apply Filters
    if status_filter:
        df = df[df["Status Code"].isin(status_filter)]
    if "Word Count" in df.columns:
        df = df[(df["Word Count"] >= min_word_count) & (df["Word Count"] <= max_word_count)]
    if "Crawl Depth" in df.columns:
        df = df[df["Crawl Depth"] <= max_crawl_depth]
    if "Unique Inlinks" in df.columns:
        df = df[(df["Unique Inlinks"] >= min_unique_inlinks) & (df["Unique Inlinks"] <= max_unique_inlinks)]
    
    st.subheader("Internal Pages Overview")
    st.dataframe(df)
    
    # Display Metrics
    total_pages = len(df)
    missing_title = df["Title 1"].isna().sum() if "Title 1" in df.columns else 0
    missing_description = df["Meta Description 1"].isna().sum() if "Meta Description 1" in df.columns else 0
    
    st.write(f"**Total Pages:** {total_pages}")
    st.write(f"**Pages Missing Title:** {missing_title}")
    st.write(f"**Pages Missing Description:** {missing_description}")

    # Status Code Distribution
    if "Status Code" in df.columns:
        st.subheader("Status Code Distribution")
        status_counts = df["Status Code"].value_counts().reset_index()
        status_counts.columns = ["Status Code", "Count"]
        fig = px.bar(status_counts, x="Status Code", y="Count", title="Status Code Distribution")
        st.plotly_chart(fig)
    
    # Word Count Distribution
    if "Word Count" in df.columns:
        st.subheader("Word Count Distribution")
        fig = px.histogram(df, x="Word Count", nbins=20, title="Word Count Distribution")
        st.plotly_chart(fig)
    
    # Internal Linking Depth
    if "Crawl Depth" in df.columns:
        st.subheader("Crawl Depth Analysis")
        depth_counts = df["Crawl Depth"].value_counts().reset_index()
        depth_counts.columns = ["Crawl Depth", "Count"]
        fig = px.bar(depth_counts, x="Crawl Depth", y="Count", title="Crawl Depth Distribution")
        st.plotly_chart(fig)
    
    # Unique Inlinks Distribution
    if "Unique Inlinks" in df.columns:
        st.subheader("Unique Inlinks Analysis")
        inlinks_counts = df["Unique Inlinks"].value_counts().reset_index()
        inlinks_counts.columns = ["Unique Inlinks", "Count"]
        fig = px.bar(inlinks_counts, x="Unique Inlinks", y="Count", title="Unique Inlinks Distribution")
        st.plotly_chart(fig)
    
    st.success("CSV Data Processed Successfully!")
else:
    st.write("Upload a Screaming Frog export CSV file to begin analysis.")
