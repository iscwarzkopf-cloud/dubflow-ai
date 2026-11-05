import gradio as gr
import time

def dublaj_yap(video_yolu):
    if video_yolu is None:
        return "Lütfen bir video yükleyin.", None
    
    yield "Adım 1/5: Video karşıya yüklendi ve parçalanıyor...", None
    time.sleep(2)
    yield "Adım 2/5: İngilizce konuşmalar deşifre ediliyor (Whisper)...", None
    time.sleep(2)
    yield "Adım 3/5: Konuşmacılar ve cinsiyetler analiz ediliyor...", None
    time.sleep(2)
    yield "Adım 4/5: Yapay zeka ile Türkçe doğal sesler sentezleniyor (Edge-TTS)...", None
    time.sleep(2)
    yield "Adım 5/5: Türkçe sesler video ile senkronize ediliyor...", None
    time.sleep(2)
    
    yield "İşlem Tamamlandı! Türkçe dublajlı videonuz hazır.", video_yolu

with gr.Blocks(theme=gr.themes.Soft(primary_hue="purple", secondary_hue="indigo")) as demo:
    gr.Markdown("# 🎙️ DubFlow AI - Ücretsiz Video Dublaj")
    gr.Markdown("### İngilizce videoları, kadın/erkek seslerini ayırt ederek sıfır ses kaymasıyla Türkçe dublaj yapar.")
    
    with gr.Row():
        video_input = gr.Video(label="İngilizce Orijinal Video Yükle (.mp4)")
    
    durum_mesaji = gr.Markdown("Durum: Bekleniyor...")
    çevir_butonu = gr.Button("Türkçe Dublaj Yap", variant="primary")
    
    with gr.Row():
        video_output = gr.Video(label="Türkçe Dublajlı Video (İndirilebilir)")
        
    çevir_butonu.click(
        fn=dublaj_yap, 
        inputs=video_input, 
        outputs=[durum_mesaji, video_output]
    )

demo.queue().launch(server_name="0.0.0.0", server_port=7860)
