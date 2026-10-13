import os
import tempfile
import threading
import time
import uuid
import warnings
from pathlib import Path

# Pygame'in gereksiz terminal uyarılarını gizleyelim
warnings.filterwarnings("ignore", category=UserWarning)
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from google.cloud import texttospeech

# Google anahtar dosyası depoya konmaz. Önce GOOGLE_APPLICATION_CREDENTIALS ortam değişkenine,
# o yoksa projedeki git'e girmeyen credentials/google-tts.json dosyasına bakılır.
DEFAULT_CREDENTIALS = Path(__file__).resolve().parent.parent / "credentials" / "google-tts.json"


class AudioSystem:
    def __init__(self, voice_name="tr-TR-Wavenet-D", speaking_rate=1.1):
        self.client = None
        self.is_speaking = False
        self._lock = threading.Lock()

        # Wavenet-D: doğal, tok bir erkek sesi. speaking_rate=1.1 normalden %10 hızlı.
        self.voice = texttospeech.VoiceSelectionParams(language_code="tr-TR", name=voice_name)
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
        )

        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and DEFAULT_CREDENTIALS.exists():
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(DEFAULT_CREDENTIALS)

        try:
            self.client = texttospeech.TextToSpeechClient()
            pygame.mixer.init()
            print("[OK] Google Cloud TTS sistemi başarıyla başlatıldı.")
        except Exception as e:
            self.client = None
            print(
                "[KRİTİK HATA] Google TTS başlatılamadı. Anahtar dosyasını GOOGLE_APPLICATION_CREDENTIALS "
                f"ortam değişkeniyle verin ya da {DEFAULT_CREDENTIALS} yoluna koyun. Hata: {e}"
            )

    def speak(self, text):
        """Sesi arka planda üretip çalar. Cümle kabul edildiyse True, atlandıysa False döner."""
        if self.client is None:
            return False
        # Kontrol ve işaretleme tek adımda: art arda gelen iki çağrı aynı anda konuşamaz
        with self._lock:
            if self.is_speaking:
                return False
            self.is_speaking = True
        # Görüntünün donmaması için ses arka planda (thread) üretilip çalınır
        threading.Thread(target=self._run_speak, args=(text,), daemon=True).start()
        return True

    def _run_speak(self, text):
        # Windows'ta dosya kilidine takılmamak için her ses benzersiz adla geçici klasöre yazılır
        temp_path = Path(tempfile.gettempdir()) / f"smart_glasses_{uuid.uuid4().hex[:8]}.mp3"
        try:
            response = self.client.synthesize_speech(
                input=texttospeech.SynthesisInput(text=text),
                voice=self.voice,
                audio_config=self.audio_config,
            )
            temp_path.write_bytes(response.audio_content)

            pygame.mixer.music.load(str(temp_path))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.unload()  # Dosyayı serbest bırak
        except Exception as e:
            print(f"[SES HATA] Google TTS işlem hatası: {e}")
        finally:
            self.is_speaking = False
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
