from google.cloud import texttospeech
import os


# İstemciyi oluştur
client = texttospeech.TextToSpeechClient()

# Seslendirilecek metin
synthesis_input = texttospeech.SynthesisInput(text="Merhaba! Akıllı gözlük projen için ses sistemi başarıyla çalışıyor.")

# Ses ayarları (Türkçe ve net bir ses seçimi)
voice = texttospeech.VoiceSelectionParams(
    language_code="tr-TR",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

# Ses dosyası formatı
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# API'ye isteği gönder
print("Ses sentezleniyor...")
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# Çıktıyı dosyaya yaz
with open("deneme.mp3", "wb") as out:
    out.write(response.audio_content)
    print('Başarılı! "deneme.mp3" dosyası oluşturuldu.')