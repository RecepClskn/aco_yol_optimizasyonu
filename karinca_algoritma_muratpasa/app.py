#Ad: Recep
#Soyad: Çalışkan
#Numara: 2312721004
#Github Repo: https://github.com/RecepClskn/aco_yol_optimizasyonu.git

import os
from pathlib import Path
from dotenv import load_dotenv

# .env dosyasını app.py ile aynı klasörden zorla oku
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

from aco import ant_colony_optimization
from maps import make_gmaps_client, geocode_addresses, build_distance_matrix_km


def get_api_key():
    key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        st.error("❌ API key yok (.env okunamadı). Proje klasöründe .env olmalı.")
        st.stop()
    return key


default_addresses = "\n".join([
    "Zemin Depo Muratpaşa Turgut Özal Mh. Gazi Bulvarı, Antalya",
    "Varlık, 175. Sk., 07000 Muratpaşa/Antalya",
    "Güden ve, Yıldız, Piri Reis Cd., 07000 Muratpaşa/Antalya",
    "Yıldız, Yıldız Cd., 07050 Muratpaşa/Antalya",
    "Altındağ, Güllük Cd., 07000 Muratpaşa/Antalya",
    "Muratpaşa, Tonguç Cd., 07000 Muratpaşa/Antalya",
    "Cumhuriyet, 625. Sk. No:16, 07010 Muratpaşa/Antalya",
    "Dutlubahçe, Fatih Cd., 07000 Muratpaşa/Antalya",
    "Etiler, Karacaoğlan Cd., 07000 Muratpaşa/Antalya",
    "Muratpaşa, 569. Sk. No:71, 07010 Muratpaşa/Antalya",
    "Muratpaşa Mah.562 Sok.Aydıcan, Apt 2, 07000 Muratpaşa/Antalya",
    "Muratpaşa, Çatalköprü Cd. 31/A, 07000 Muratpaşa/Antalya",
    "Deniz, 122. Sk., 07000 Muratpaşa/Antalya",
    "Haşimişcan, Arık Cd. 10a, 07100 Muratpaşa/Antalya",
    "Gençlik, Fevzi Çakmak Cd., 07000 Muratpaşa/Antalya",
    "Yeşilbahçe, 1466. Sk., 07000 Muratpaşa/Antalya",
    "Meydankavağı, 1561. Sk. 25A A-B, 07000 Muratpaşa/Antalya",
    "Kırcami, Avni Tolunay Cd. No:14, 07000 Muratpaşa/Antalya",
    "Şirinyalı, 1486. Sk. A-B, 07000 Muratpaşa/Antalya",
    "Kızıltoprak, Şht. Ercan Cd., 07000 Muratpaşa/Antalya",
])


@st.cache_data(show_spinner=False)
def cached_geocode(api_key: str, names: list[str], addresses: list[str]):
    gmaps = make_gmaps_client(api_key)
    return geocode_addresses(gmaps, names, addresses)


def cached_distance(api_key: str, locs):
    gmaps = make_gmaps_client(api_key)
    return build_distance_matrix_km(gmaps, locs)




def main():
    st.set_page_config(layout="wide")
    st.title("🐜 Karınca Kolonisi Algoritması ile Kargo Rota Optimizasyonu")
    st.caption("Antalya / Muratpaşa – Depodan başlayıp 20 mağazayı ziyaret eden en kısa tur")

    #Sidebar Parametreler
    st.sidebar.header("ACO Parametreleri (Ayarlanabilir)")

    ants = st.sidebar.slider("Karınca Sayısı", 10, 200, 60, step=5)
    iters = st.sidebar.slider("İterasyon Sayısı", 20, 500, 200, step=10)

    alpha = st.sidebar.slider("α (Feromon etkisi)", 0.1, 5.0, 1.0, step=0.1)
    beta = st.sidebar.slider("β (Sezgisel/1-D etkisi)", 0.1, 10.0, 3.0, step=0.1)
    rho = st.sidebar.slider("Buharlaşma oranı (ρ)", 0.01, 0.90, 0.50, step=0.01)

    st.sidebar.caption("İpucu: β arttıkça yakın mesafeler daha fazla seçilir. ρ arttıkça feromon daha hızlı buharlaşır.")

    #Adres girişi
    st.subheader("📍 Lokasyon Listesi (İlk satır Depo)")
    addr_text = st.text_area("Her satıra bir adres", default_addresses, height=260)

    api_key = get_api_key()

    #Koordinatları al
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📌 1) Koordinatları Al (Geocode)", use_container_width=True):
            addresses = [a.strip() for a in addr_text.splitlines() if a.strip()]
            if len(addresses) < 2:
                st.error("En az 2 adres gir (1 depo + 1 mağaza).")
                st.stop()

            names = ["Depo"] + [f"Mağaza {i}" for i in range(1, len(addresses))]
            locs = cached_geocode(api_key, names, addresses)
            st.session_state["locs"] = locs
            st.success(f"✅ {len(locs)} lokasyon için koordinatlar alındı.")

    #Mesafe matrisi + ACO
    with col2:
        if st.button("📦 2-3) Mesafe Matrisi + ACO Çalıştır", use_container_width=True):
            if "locs" not in st.session_state:
                st.error("Önce 'Koordinatları Al' butonuna bas.")
                st.stop()

            locs = st.session_state["locs"]
            D = cached_distance(api_key, locs)

            tour, dist, history = ant_colony_optimization(
                D,
                n_ants=ants,
                n_iter=iters,
                alpha=alpha,
                beta=beta,
                rho=rho,
                start_index=0
            )

            st.session_state["tour"] = tour
            st.session_state["dist"] = dist
            st.session_state["history"] = history
            st.success("✅ ACO tamamlandı.")

    #Sonuçlar
    if "tour" in st.session_state:
        locs = st.session_state["locs"]
        tour = st.session_state["tour"]
        dist = st.session_state["dist"]
        history = st.session_state["history"]

        st.subheader("📊 Sonuçlar")
        st.success(f"✅ En Kısa Mesafe: {dist:.2f} km")

        #Grafik
        st.subheader("📈 İterasyonlara Göre En Kısa Mesafe")
        fig, ax = plt.subplots()
        ax.plot(history)
        ax.set_xlabel("İterasyon")
        ax.set_ylabel("En iyi mesafe (km)")
        st.pyplot(fig)

        #Ziyaret sırası
        st.subheader("📋 Ziyaret Sırası (Depodan Başlayarak)")
        order_names = []
        for idx in tour:
            if idx == 0:
                order_names.append("Depo")
            else:
                order_names.append(f"Mağaza {idx}")
        st.write(" → ".join(order_names))

        #Harita
        st.subheader("🗺️ En Kısa Yolun Harita Üzerinde Çizimi")
        m = folium.Map(location=[locs[0].lat, locs[0].lng], zoom_start=12)

        # Depo (mavi)
        folium.Marker(
            [locs[0].lat, locs[0].lng],
            icon=folium.Icon(color="blue", icon="home"),
            tooltip="Depo"
        ).add_to(m)

        # Mağazalar (kırmızı)
        for i in range(1, len(locs)):
            folium.Marker(
                [locs[i].lat, locs[i].lng],
                icon=folium.Icon(color="red", icon="shopping-cart"),
                tooltip=f"Mağaza {i}"
            ).add_to(m)

        # Rota çizimi
        path = [[locs[i].lat, locs[i].lng] for i in tour]
        folium.PolyLine(path, weight=4).add_to(m)

        st_folium(m, width=1000, height=520)


if __name__ == "__main__":
    main()
