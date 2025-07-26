import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Titel
st.title("Porsche 911 Cabriolet Finder")

# Filtre
max_price = st.slider("Maks pris (DKK)", 100000, 2000000, 2000000, step=50000)
min_year = st.slider("Minimum årgang", 1950, 2024, 2024)
max_km = st.slider("Maks km", 0, 300000, 300000, step=5000)

# Funktion til at scrape eksempler fra Bilbasen (demo med fast URL for Porsche 911)
def fetch_bilbasen_listings():
    url = "https://www.bilbasen.dk/brugt/bil/ps-porsche_911_cabriolet"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    cars = []
    listings = soup.find_all("a", class_="listing-link")

    for listing in listings[:10]:  # Begræns til 10 resultater for demo
        title = listing.find("h2")
        if not title:
            continue
        link = "https://www.bilbasen.dk" + listing["href"]
        car_info = title.text.strip()
        cars.append({"Titel": car_info, "Link": link})

    return pd.DataFrame(cars)

# Hent data og vis resultater
if st.button("Find biler"):
    with st.spinner("Henter bilopslag ..."):
        df = fetch_bilbasen_listings()
        st.success(f"Fandt {len(df)} opslag!")
        st.dataframe(df)
        for _, row in df.iterrows():
            st.markdown(f"[{row['Titel']}]({row['Link']})")

st.caption("Prototype: Viser kun et udsnit af faktiske opslag (til test og demo)")
