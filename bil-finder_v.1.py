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
    # Dummy-data til demo
    cars = [
        {
            "Titel": "Porsche 911 Cabriolet 3.8 Turbo S 2016 – 58.000 km – 975.000 kr.",
            "Link": "https://www.dba.dk/link1"
        },
        {
            "Titel": "Porsche 911 Cabriolet 3.0 Carrera 2018 – 47.000 km – 899.000 kr.",
            "Link": "https://www.dba.dk/link2"
        },
        {
            "Titel": "Porsche 911 Cabriolet 3.6 Carrera 4 2015 – 91.000 km – 789.000 kr.",
            "Link": "https://www.dba.dk/link3"
        },
        {
            "Titel": "Porsche 911 Cabriolet Turbo 2020 – 38.000 km – 1.049.000 kr.",
            "Link": "https://www.dba.dk/link4"
        },
    ]

    # Filtrering baseret på input
    filtered = []
    for car in cars:
        title = car["Titel"]
        price = int(''.join(filter(str.isdigit, title.split("kr.")[0][-9:])))
        km_str = ''.join(filter(str.isdigit, title.split("km")[0].split()[-2]))
        km = int(km_str) if km_str else 0
        year = int([s for s in title.split() if s.isdigit() and len(s) == 4][0])

        if price > max_price or km > max_km or year < min_year:
            continue
        filtered.append(car)

    return pd.DataFrame(filtered)

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
