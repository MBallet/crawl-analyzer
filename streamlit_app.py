import streamlit as st
import pandas as pd
import plotly.express as px
import os
import tempfile

# Streamlit App Title with Image
st.set_page_config(page_title="Screaming Frogger", page_icon=":frog:")
st.image("Frog - open.png", width=500) 
st.title("Screaming Frog CSV Analyzer")


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
    content_type_filter = st.sidebar.multiselect("Filter by Content Type", df["Content Type"].unique()) if "Content Type" in df.columns else []
    min_word_count, max_word_count = st.sidebar.slider("Filter by Word Count Range", int(df["Word Count"].min()), int(df["Word Count"].max()), (int(df["Word Count"].min()), int(df["Word Count"].max()))) if "Word Count" in df.columns else (0, 0)
    max_crawl_depth = st.sidebar.slider("Filter by Maximum Crawl Depth", int(df["Crawl Depth"].min()), int(df["Crawl Depth"].max()), int(df["Crawl Depth"].max())) if "Crawl Depth" in df.columns else 0
    min_unique_inlinks, max_unique_inlinks = st.sidebar.slider("Filter by Unique Inlinks Range", int(df["Unique Inlinks"].min()), int(df["Unique Inlinks"].max()), (int(df["Unique Inlinks"].min()), int(df["Unique Inlinks"].max()))) if "Unique Inlinks" in df.columns else (0, 0)
    
    # Apply Filters
    if status_filter:
        df = df[df["Status Code"].isin(status_filter)]
    if content_type_filter:
        df = df[df["Content Type"].isin(content_type_filter)]
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

    # Indexability Breakdown
    if "Indexability" in df.columns:
        st.subheader("Indexability Breakdown")
        indexability_counts = df["Indexability"].value_counts().reset_index()
        indexability_counts.columns = ["Indexability", "Count"]
        fig = px.pie(indexability_counts, names="Indexability", values="Count", title="Indexability Breakdown")
        st.plotly_chart(fig)
    
    # Title & Meta Description Length Distributions
    if "Title 1 Length" in df.columns:
        st.subheader("Title Length Distribution")
        fig = px.histogram(df, x="Title 1 Length", nbins=20, title="Title Length Distribution")
        st.plotly_chart(fig)
    if "Meta Description 1 Length" in df.columns:
        st.subheader("Meta Description Length Distribution")
        fig = px.histogram(df, x="Meta Description 1 Length", nbins=20, title="Meta Description Length Distribution")
        st.plotly_chart(fig)
    
    # Readability vs. Word Count
    if "Flesch Reading Ease Score" in df.columns and "Word Count" in df.columns:
        st.subheader("Readability vs. Word Count")
        fig = px.scatter(df, x="Word Count", y="Flesch Reading Ease Score", title="Readability vs. Word Count")
        st.plotly_chart(fig)
    
    # Crawl Depth vs. Link Score
    if "Crawl Depth" in df.columns and "Link Score" in df.columns:
        st.subheader("Crawl Depth vs. Link Score")
        fig = px.scatter(df, x="Crawl Depth", y="Link Score", title="Crawl Depth vs. Link Score")
        st.plotly_chart(fig)
    
    # Duplicate Content Analysis
    if "No. Near Duplicates" in df.columns:
        st.subheader("Duplicate Content Analysis")
        fig = px.histogram(df, x="No. Near Duplicates", nbins=10, title="Duplicate Content Distribution")
        st.plotly_chart(fig)
    
    st.success("CSV Data Processed Successfully!")
else:
    st.write("Upload a Screaming Frog export CSV file to begin analysis.")
