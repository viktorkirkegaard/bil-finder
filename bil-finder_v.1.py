import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Porsche 911 Finder", layout="wide")
st.title("🔍 Porsche 911 Cabriolet Finder (via DBA)")

# Inputfelter
max_price = st.slider("Maks pris (DKK)", 100000, 2000000, 2000000, step=50000)
max_km = st.slider("Maks km", 0, 300000, 300000, step=5000)
min_year = st.slider("Min. årgang", 1950, 2024, 2024)

def fetch_dba_listings():
    url = f"https://www.dba.dk/biler/soeg/?soeg=porsche+911+cabriolet&pris=(0-{max_price})&sort=listingdate-desc"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error(f"Kunne ikke hente data fra DBA (statuskode: {response.status_code})")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find_all("tr", class_="dbaListing")

    if not listings:
        st.warning("Ingen opslag fundet – DBA har måske ændret struktur.")
        return pd.DataFrame()

    cars = []
    for listing in listings:
        link_tag = listing.find("a", href=True)
        if not link_tag:
            continue
        title = link_tag.get_text(strip=True)
        link = "https://www.dba.dk" + link_tag["href"]

        # Simpel filtrering: check om årstal og km står i teksten
        if str(min_year) not in title and str(min_year + 1) not in title:
            continue
        if "km" in title.lower():
            km_str = ''.join(filter(str.isdigit, title))
            if km_str and int(km_str) > max_km:
                continue

        cars.append({"Titel": title, "Link": link})

    return pd.DataFrame(cars)

if st.button("🔎 Find biler"):
    with st.spinner("Henter bilopslag fra DBA..."):
        df = fetch_dba_listings()
        if df.empty:
            st.error("Ingen relevante biler fundet.")
        else:
            st.success(f"Fandt {len(df)} bil(er)")
            st.dataframe(df)
            for _, row in df.iterrows():
                st.markdown(f"- [{row['Titel']}]({row['Link']})")
