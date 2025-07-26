import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bilvælger", layout="wide")
st.title("🚘 Bilvælger – Find brugte biler (demo)")

# Mærker og modeller (du kan tilføje flere selv)
car_data = {
    "Porsche": ["911", "Cayenne", "Panamera", "Taycan"],
    "Audi": ["A3", "A4", "A6", "Q5", "Q7"],
    "BMW": ["1-serie", "3-serie", "5-serie", "X3", "X5"],
    "Mercedes": ["C-Klasse", "E-Klasse", "GLC", "S-Klasse"],
    "Volkswagen": ["Golf", "Passat", "Tiguan", "Polo"],
}

# Brugerens valg
brand = st.selectbox("Vælg mærke", list(car_data.keys()))
model = st.selectbox("Vælg model", car_data[brand])

# Filtre
max_price = st.slider("Maks pris (DKK)", 100000, 2000000, 1000000, step=50000)
max_km = st.slider("Maks km", 0, 300000, 100000, step=5000)
min_year = st.slider("Min. årgang", 1990, 2024, 2014)

# Dummy-data til test (kan senere erstattes med rigtig scraping)
dummy_data = [
    {"Titel": "Porsche 911 Cabriolet 2016 – 58.000 km – 975.000 kr.", "Link": "https://dba.dk/p1"},
    {"Titel": "Porsche Cayenne 2018 – 78.000 km – 699.000 kr.", "Link": "https://dba.dk/p2"},
    {"Titel": "Audi A6 2019 – 65.000 km – 529.000 kr.", "Link": "https://dba.dk/a6"},
    {"Titel": "BMW X5 2020 – 42.000 km – 849.000 kr.", "Link": "https://dba.dk/x5"},
    {"Titel": "Mercedes E-Klasse 2015 – 115.000 km – 349.000 kr.", "Link": "https://dba.dk/e"},
    {"Titel": "Volkswagen Golf 2021 – 35.000 km – 269.000 kr.", "Link": "https://dba.dk/golf"},
]

# Funktion til filtrering
def filter_listings(brand, model):
    filtered = []
    for car in dummy_data:
        title = car["Titel"].lower()
        if brand.lower() not in title or model.lower() not in title:
            continue

        # Pris
        try:
            price_str = car["Titel"].split("kr.")[-1].replace(".", "").strip()
            price = int(''.join(filter(str.isdigit, price_str)))
        except:
            price = 9999999

        # Kilometer
        try:
            km_str = car["Titel"].split("km")[0].split("–")[-1].strip()
            km = int(''.join(filter(str.isdigit, km_str)))
        except:
            km = 9999999

        # Årgang
        try:
            year = int([s for s in title.split() if s.isdigit() and len(s) == 4][0])
        except:
            year = 1900

        # Filtrering
        if price <= max_price and km <= max_km and year >= min_year:
            filtered.append(car)

    return pd.DataFrame(filtered)

# Vis resultater
if st.button("🔍 Find biler"):
    with st.spinner("Henter resultater..."):
        df = filter_listings(brand, model)
        if df.empty:
            st.error("Ingen biler fundet, prøv at justere dine filtre.")
        else:
            st.success(f"Fandt {len(df)} bil(er)")
            st.dataframe(df)
            for _, row in df.iterrows():
                st.markdown(f"- [{row['Titel']}]({row['Link']})")
