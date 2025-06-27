
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="🚵 MTB Club Grant Finder")
st.title("🚵 MTB Club Grant Finder")

# Real-time scraper for Brisbane City Council Grants
def scrape_brisbane_grants():
    url = "https://www.brisbane.qld.gov.au/community-support-and-safety/grants-and-sponsorship"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    grants = []

    for link in soup.select(".field-content a"):
        title = link.get_text(strip=True)
        href = link.get("href")
        if not href.startswith("http"):
            href = "https://www.brisbane.qld.gov.au" + href

        if "grant" in title.lower():
            grants.append({
                "Title": title,
                "Description": "Details available on the linked page.",
                "Region": "Brisbane",
                "URL": href,
                "Tags": "community, Brisbane"
            })

    return grants

# Load data
grants = scrape_brisbane_grants()
df = pd.DataFrame(grants)

# UI
search = st.text_input("🔍 Search by keyword (e.g. cycling, Brisbane, sponsorship)")

if search:
    df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)]

if not df.empty:
    st.dataframe(df[["Title", "Region", "Tags"]])

    for _, row in df.iterrows():
        with st.expander(row["Title"]):
            st.markdown(f"**Region:** {row['Region']}")
            st.markdown(f"**[View Grant Details]({row['URL']})**")
            st.write(row['Description'])
else:
    st.warning("⚠️ No grant data found. The Brisbane City Council site may have changed or is temporarily unavailable.")

st.markdown("---")
st.caption("Data sourced live from brisbane.qld.gov.au")
