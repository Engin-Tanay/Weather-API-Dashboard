import streamlit as st
import requests
import os
# Sayfa ayarı
st.set_page_config(
    page_title="Weather App",
    layout="centered"
)

st.title("🌤️ Weather API Dashboard")

# Kullanıcıdan şehir alma
city = st.text_input("Şehir gir (örn: Antalya, Istanbul)")

# API KEY (BURAYA KENDİ KEY'İNİ YAZ)


API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Kullanıcı şehir girerse çalışsın
if city:

    # API URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    # API isteği
    response = requests.get(url)
    data = response.json()

    # Hata kontrolü
    if data.get("cod") != 200:
        st.error("Şehir bulunamadı veya API hatası!")
    else:
        # Veriler
        city_name = data["name"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        # Gösterim
        st.subheader(f"📍 {city_name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🌡️ Sıcaklık", f"{temp} °C")

        with col2:
            st.metric("🤒 Hissedilen", f"{feels_like} °C")

        with col3:
            st.metric("💧 Nem", f"{humidity}%")

        st.write(f"☁️ Durum: **{weather}**")