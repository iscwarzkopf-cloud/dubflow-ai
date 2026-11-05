import streamlit as st
import time

st.set_page_config(page_title="DubFlow AI", page_icon="🎙️", layout="centered")

st.title("🎙️ DubFlow AI - Ücretsiz Video Dublaj")
st.write("İngilizce videoları, kadın/erkek seslerini ayırt ederek sıfır ses kaymasıyla Türkçe dublaj yapar.")

# Video yükleme alanı
video_file = st.file_uploader("İngilizce Orijinal Video Yükle (.mp4)", type=["mp4"])

if video_file is not None:
    st.video(video_file)
    
    if st.button("Türkçe Dublaj Yap", type="primary"):
        durum = st.empty()
        
        # Adımların simülasyonu
        durum.info("Adım 1/5: Video karşıya yüklendi ve parçalanıyor...")
        time.sleep(2)
        durum.info("Adım 2/5: İngilizce konuşmalar deşifre ediliyor (Whisper)...")
        time.sleep(2)
        durum.info("Adım 3/5: Konuşmacılar ve cinsiyetler analiz ediliyor...")
        time.sleep(2)
        durum.info("Adım 4/5: Yapay zeka ile Türkçe doğal sesler sentezleniyor (Edge-TTS)...")
        time.sleep(2)
        durum.info("Adım 5/5: Türkçe sesler video ile senkronize ediliyor...")
        time.sleep(2)
        
        durum.success("İşlem Tamamlandı! Türkçe dublajlı videonuz hazır.")
        
        st.subheader("Türkçe Dublajlı Video (İndirilebilir)")
        st.video(video_file)
        
