import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Page config
st.set_page_config(page_title="MTB Club Grant Finder", layout="wide")
st.title("🚵 MTB Club Grant Finder")

st.markdown("""
This tool automatically scrapes public grant websites and displays relevant opportunities for your Mountain Bike Club.
""")

# Dummy scraper function
def scrape_dummy_grants():
    return [
        {
            "Title": "Community Sport Infrastructure Grant",
            "URL": "https://example.com/grant1",
            "Source": "SportAus",
            "Tags": "cycling, youth",
            "Deadline": "2025-09-30",
            "Description": "Funding for local clubs upgrading sports facilities."
        },
        {
            "Title": "Active Clubs Kickstart Program",
            "URL": "https://example.com/grant2",
            "Source": "QLD Gov",
            "Tags": "equipment, training",
            "Deadline": "2025-10-15",
            "Description": "Support for sports equipment and coaching costs."
        }
    ]

# Load and display grants
grants = scrape_dummy_grants()
df = pd.DataFrame(grants)

search_term = st.text_input("🔍 Search by keyword (e.g. 'cycling', 'equipment')")

if search_term:
    df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)]

st.dataframe(df[["Title", "Source", "Tags", "Deadline"]])

for _, row in df.iterrows():
    with st.expander(row["Title"]):
        st.markdown(f"**Deadline**: {row['Deadline']}")
        st.markdown(f"**Source**: {row['Source']}")
        st.markdown(f"**Tags**: {row['Tags']}")
        st.markdown(f"**[Apply Here]({row['URL']})**")
        st.markdown(f"{row['Description']}")

# Footer
st.markdown("---")
st.caption("Built for MTB clubs to find relevant grants with ease.")
