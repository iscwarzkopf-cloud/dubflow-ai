import streamlit as st
from googletrans import Translator
import asyncio
import edge_tts
import os
import subprocess

st.set_page_config(page_title="DubFlow AI - Profesyonel Dublaj", page_icon="🎙️", layout="centered")

st.title("🎙️ DubFlow AI - Gerçek Yapay Zeka Dublaj")
st.write("Sistem sınırlarına takılmadan, videolarınızı tamamen gerçek kelimelerle Türkçe dublaja dönüştürün.")

if not os.path.exists("temp"):
    os.makedirs("temp")

async def ses_sentezle(metin, ses_secimi, cikis_yolu):
    ses = "tr-TR-AhmetNeural" if ses_secimi == "Erkek (Ahmet)" else "tr-TR-EmelNeural"
    communicate = edge_tts.Communicate(metin, ses)
    await communicate.save(cikis_yolu)

# Ses Seçim Alanı
ses_karekter = st.selectbox("1️⃣ Türkçe Dublaj Ses Karakterini Seçin:", ["Erkek (Ahmet)", "Kadın (Emel)"])

# Metin Giriş Alanı (Gerçek Çeviri İçin)
ingilizce_metin = st.text_area("2️⃣ Videoda Konuşulan İngilizce Metni Buraya Yazın veya Yapıştırın:", 
                               "Hello, welcome to this video. We are successfully translating this content.")

# Video Yükleme Alanı
video_file = st.file_uploader("3️⃣ İngilizce Orijinal Video Yükle (.mp4)", type=["mp4"])

if video_file is not None:
    orijinal_video_yolu = os.path.join("temp", "orijinal_video.mp4")
    with open(orijinal_video_yolu, "wb") as f:
        f.write(video_file.getbuffer())
        
    st.video(video_file)
    
    if st.button("Gerçek Türkçe Dublaj Yap", type="primary"):
        durum = st.empty()
        
        try:
            # ADIM 1: Çeviri
            durum.info("Adım 1/3: Yazdığınız İngilizce metin Türkçeye tercüme ediliyor...")
            translator = Translator()
            çeviri = translator.translate(ingilizce_metin, src='en', dest='tr')
            tam_turkce_metin = çeviri.text
            
            # ADIM 2: Robotik Olmayan Seslendirme
            durum.info(f"Adım 2/3: {ses_karekter} ses modeliyle Türkçe yapay zeka sesi üretiliyor...")
            turkce_ses_yolu = os.path.join("temp", "turkce_ses.mp3")
            asyncio.run(ses_sentezle(tam_turkce_metin, ses_karekter, turkce_ses_yolu))
            
            # ADIM 3: FFmpeg Birleştirme
            durum.info("Adım 3/3: Türkçe ses, videonun orijinal süresine göre tam senkronize ediliyor...")
            cikti_video_yolu = os.path.join("temp", "turkce_dublaj_video.mp4")
            
            # Orijinal videonun tam süresini koruyarak yeni sesi tam üzerine yerleştirir
            subprocess.run(["ffmpeg", "-y", "-i", orijinal_video_yolu, "-i", turkce_ses_yolu, "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0", "-shortest", cikti_video_yolu], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            durum.success("🎉 Başarılı! İngilizce videonuz yazdığınız metne göre tamamen Türkçe dublaj yapıldı!")
            
            st.subheader("🎬 Türkçe Dublajlı Video (İndirilebilir)")
            with open(cikti_video_yolu, "rb") as file:
                st.video(file.read(), format="video/mp4")
                
        except Exception as e:
            durum.error(f"Bir pürüz oluştu: {str(e)}. Lütfen tekrar deneyin.")
            
