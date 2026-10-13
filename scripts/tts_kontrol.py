"""Google Cloud TTS bağlantısını elle denemek için: python scripts/tts_kontrol.py

Gerçek bir API isteği gönderir ve deneme.mp3 dosyası oluşturur. Otomatik test değildir.
Anahtar dosyası src/audio.py ile aynı şekilde bulunur (ortam değişkeni ya da credentials/google-tts.json).
"""
import os
from pathlib import Path

from google.cloud import texttospeech

DEFAULT_CREDENTIALS = Path(__file__).resolve().parent.parent / "credentials" / "google-tts.json"


def main():
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and DEFAULT_CREDENTIALS.exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(DEFAULT_CREDENTIALS)

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text="Merhaba! Akıllı gözlük projen için ses sistemi başarıyla çalışıyor.")
    voice = texttospeech.VoiceSelectionParams(language_code="tr-TR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    print("Ses sentezleniyor...")
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    Path("deneme.mp3").write_bytes(response.audio_content)
    print('Başarılı! "deneme.mp3" dosyası oluşturuldu.')


if __name__ == "__main__":
    main()
