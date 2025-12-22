#Karınca Kolonisi Algoritması ile Kargo Rota Optimizasyonu
#Recep Çalışkan 2312721004

Bu projede, Antalya / Muratpaşa ilçesinde bulunan bir depo ve 20 mağaza için
en kısa kargo dağıtım rotası, **Karınca Kolonisi Algoritması (ACO)** kullanılarak
hesaplanmıştır.

Gerçek yol mesafeleri Google Maps API üzerinden alınmış
ve sonuçlar Streamlit arayüzü ile görselleştirilmiştir.

Bu projede kullandığımız teknolojiler ve kütüphanelerin bazıları (İndirmemiz gerekenler requirements.txt dosyasında var)
- Python
- Streamlit
- Google Maps API
- Folium
- Matplotlib
- NumPy

Proje Özellikleri
- Adreslerden koordinat alma (Geocoding)
- Google Maps ile mesafe matrisi oluşturma
- ACO ile en kısa turun bulunması
- Ayarlanabilir ACO parametreleri (karınca sayısı, iterasyon, α, β, ρ)
- En kısa yolun harita üzerinde çizimi
- İterasyonlara göre mesafe grafiği

Kurulum
Klasörün içindeki terminale girerek bu kodu yazıyoruz.
pip install -r requirements.txt"

API Key için ise Google Cloud Console'dan ücretsiz deneme sürümüyle giriş yaparak API Keyimizi rahatlıkla alabiliriz.
Bu API Key'i streamlit içindeki secrets.toml ya da .env dosyamıza dosyalarda olduğu gibi yazmamız gerekiyor.

Daha sonra tüm işlemleri tamamlayınca önce .\.venv\Scripts\activate ile giriş yapıp daha sonra python -m streamlit run app.py yazarak streamlitimizi çalıştırabiliriz.
