
import pandas as pd
import streamlit as st
import os
from transformers import pipeline
pip install torch

st.set_page_config(page_title="Rental Price Analytics", layout="wide")
st.title("🏠 Rental Price Analytics Dashboard + AI Advisor")

# Load or scrape rental data
data_file = "data/rentals.csv"

def get_llm():
    return pipeline("text2text-generation", model="google/flan-t5-base")

llm = get_llm()

if not os.path.exists(data_file):
    st.warning("No rental data found. Run scraper.py first.")
else:
    df = pd.read_csv(data_file)
    pincode = st.selectbox("Pincode", sorted(df["pincode"].unique()))
    flat_type = st.selectbox("Flat Type", sorted(df["flat_type"].unique()))

    filtered = df[(df["pincode"] == pincode) & (df["flat_type"] == flat_type)]

    if not filtered.empty:
        st.subheader("💰 Rent Price Summary")
        desc = filtered["rent"].describe(percentiles=[.1, .25, .5, .75, .9])
        st.write(desc)

        st.subheader("📅 Trend Over Time")
        trend = filtered.groupby("posted_on")["rent"].median()
        st.line_chart(trend)

        st.subheader("🌟 Popular Amenities")
        amenities = filtered["amenities"].str.split(", ").explode().value_counts().head(10)
        st.bar_chart(amenities)

        st.subheader("🧠 Smart Rent Advisor")
        example_row = filtered.sample(1).iloc[0]
        rent = example_row["rent"]
        area = example_row["area"]
        furnishing = example_row["furnishing"]
        amenities_list = example_row["amenities"]
        month = example_row["posted_on"]
        low = int(desc["10%"])
        high = int(desc["90%"])
        context = f"""
        Flat type: {flat_type}, Area: {area} sqft, Rent: ₹{rent},
        Furnishing: {furnishing}, Amenities: {amenities_list},
        Expected Band: ₹{low}–₹{high}, Month: {month}
        """
        prompt = f"Is this listing fairly priced? Justify: {context}"

        if st.button("Check AI Opinion"):
            with st.spinner("Analyzing with AI..."):
                result = llm(prompt, max_length=100)[0]["generated_text"]
                st.success(result)
    else:
        st.warning("No data for this filter.")
