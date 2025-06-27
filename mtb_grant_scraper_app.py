import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="🚵 MTB Club Grant Finder")
st.title("🚵 MTB Club Grant Finder")

# Real-time scraper for ClubGrants
def scrape_clubgrants():
    url = "https://www.clubgrants.com.au/find-your-local-grant"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    grants = []

    for row in soup.select(".find-your-local-grant__listing-item"):
        title = row.select_one(".find-your-local-grant__title").get_text(strip=True)
        summary = row.select_one(".find-your-local-grant__description").get_text(strip=True)
        region = row.select_one(".find-your-local-grant__location").get_text(strip=True)
        link = "https://www.clubgrants.com.au" + row.select_one("a")["href"]

        grants.append({
            "Title": title,
            "Description": summary,
            "Region": region,
            "URL": link,
            "Tags": "community, club"
        })

    return grants

# Load data
grants = scrape_clubgrants()
df = pd.DataFrame(grants)

# UI
search = st.text_input("🔍 Search by keyword (e.g. cycling, region, equipment)")

if search:
    df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)]

st.dataframe(df[["Title", "Region", "Tags"]])

for _, row in df.iterrows():
    with st.expander(row["Title"]):
        st.markdown(f"**Region:** {row['Region']}")
        st.markdown(f"**[View Grant Details]({row['URL']})**")
        st.write(row['Description'])

st.markdown("---")
st.caption("Data sourced live from ClubGrants.com.au")
