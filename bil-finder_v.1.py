import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Bilvælger", layout="wide")
st.title("🚘 Bilvælger – Find brugte biler")

# 1. Mærker og modeller
car_data = {
    "Porsche": ["911", "Cayenne", "Panamera", "Taycan"],
    "Audi": ["A3", "A4", "A6", "Q5", "Q7"],
    "BMW": ["1-serie", "3-serie", "5-serie", "X3", "X5"],
    "Mercedes": ["C-Klasse", "E-Klasse", "GLC", "S-Klasse"],
    "Volkswagen": ["Golf", "Passat", "Tiguan", "Polo"],
}

# 2. Bruger vælger mærke og model
brand = st.selectbox("Vælg mærke", list(car_data.keys()))
model = st.selectbox("Vælg model", car_data[brand])

# Inputfelter
max_price = st.slider("Maks pris (DKK)", 100000, 2000000, 2000000, step=50000)
max_km = st.slider("Maks km", 0, 300000, 300000, step=5000)
min_year = st.slider("Min. årgang", 1950, 2024, 2024)


def fetch_dba_listings(brand, model):
    # Dummy-data
    all_cars = [
        {"Titel": "Porsche 911 Cabriolet 2016 – 58.000 km – 975.000 kr.", "Link": "https://dba.dk/p1"},
        {"Titel": "Porsche Cayenne 2018 – 78.000 km – 699.000 kr.", "Link": "https://dba.dk/p2"},
        {"Titel": "Audi A6 2019 – 65.000 km – 529.000 kr.", "Link": "https://dba.dk/a6"},
        {"Titel": "BMW X5 2020 – 42.000 km – 849.000 kr.", "Link": "https://dba.dk/x5"},
        {"Titel": "Mercedes E-Klasse 2015 – 115.000 km – 349.000 kr.", "Link": "https://dba.dk/e"},
    ]

    filtered = []
    for car in all_cars:
        title = car["Titel"].lower()
        if brand.lower() not in title or model.lower() not in title:
            continue

        price = int(''.join(filter(str.isdigit, title.split("kr.")[-1])))
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
