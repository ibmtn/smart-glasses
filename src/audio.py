import os
import threading
import time
import uuid

# Pygame'in gereksiz terminal uyarılarını gizleyelim
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from google.cloud import texttospeech

class AudioSystem:
    def __init__(self, credentials_file="smart-glasses-492614-0ff024ff67db.json"):
        self.is_speaking = False
        
        try:
            # Google Cloud kimlik doğrulama dosyasını sisteme tanıtıyoruz
            current_dir = os.path.dirname(os.path.abspath(__file__))
            cred_path = os.path.join(current_dir, credentials_file)
            
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
            
            # İstemciyi (Client) ve ses çalarımızı (Pygame) başlatıyoruz
            self.client = texttospeech.TextToSpeechClient()
            pygame.mixer.init()
            print("[OK] Google Cloud TTS sistemi başarıyla başlatıldı.")
            
        except Exception as e:
            print(f"[KRİTİK HATA] Google API başlatılamadı! 'smart-glasses-492614-0ff024ff67db.json' dosyası src klasöründe mi? Hata: {e}")

    def speak(self, text):
        # Eğer zaten konuşuyorsa yeni gelen cümleyi es geç (sesler üst üste binmesin)
        if self.is_speaking:
            return

        # Görüntünün donmaması için sesi arka planda (Thread) oluşturup çalıyoruz
        thread = threading.Thread(target=self._run_speak, args=(text,))
        thread.daemon = True
        thread.start()

    def _run_speak(self, text):
        self.is_speaking = True
        
        # Windows'ta dosya kilitlenme sorununu çözmek için her sese rastgele bir isim veriyoruz
        # Örnek: temp_speech_a1b2c3.mp3
        temp_filename = f"temp_speech_{uuid.uuid4().hex[:6]}.mp3"
        
        try:
            # 1. Metni Google'a Gönder
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # 2. Ses Ayarlarını Yap (Wavenet-D: Çok doğal, tok bir erkek sesi. İstersen A, B, C, D, E yapabilirsin)
            voice = texttospeech.VoiceSelectionParams(
                language_code="tr-TR",
                name="tr-TR-Wavenet-D" 
            )
            
            # 3. Çıktı Formatı (MP3)
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.1 # Konuşma hızını biraz artırdık (%10), çok yavaş gelirse artırabilirsin
            )

            # 4. API'den Sesi Al
            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            # 5. Sesi Bilgisayara Kaydet
            with open(temp_filename, "wb") as out:
                out.write(response.audio_content)

            # 6. Sesi Çal
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()

            # Müzik bitene kadar bu Thread'i beklet
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            pygame.mixer.music.unload() # Dosyayı serbest bırak

        except Exception as e:
            print(f"[SES HATA] Google TTS İşlem Hatası: {e}")
            
        finally:
            self.is_speaking = False
            # İşimiz biten geçici MP3 dosyasını silerek klasörü temiz tut
            if os.path.exists(temp_filename):
                try:
                    os.remove(temp_filename)
                except:
                    pass

            


# import warnings
# # Gereksiz uyarıları terminalden gizler
# warnings.filterwarnings("ignore", category=UserWarning)

# import os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# # ... şimdi diğer importlar gelebilir
# import os
# import threading
# import time

# # Pygame selamlama mesajını gizle
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# import pygame

# class AudioSystem:
#     def __init__(self, use_google=False):
#         self.use_google = use_google
#         self.is_speaking = False
#         try:
#             pygame.mixer.init()
#         except Exception as e:
#             print(f"Ses sistemi başlatılamadı: {e}")

#     def speak(self, text):
#         if not self.is_speaking:
#             thread = threading.Thread(target=self._generate_and_play, args=(text,))
#             thread.daemon = True # Ana program kapanınca bu da kapansın
#             thread.start()

#     def _generate_and_play(self, text):
#         self.is_speaking = True
#         speech_file = "speech.mp3"
        
#         try:
#             # Piper veya Google ile sesi oluştur
#             if self.use_google:
#                 self._google_tts(text, speech_file)
#             else:
#                 self._piper_tts(text, speech_file)

#             # Dosya oluştu mu kontrol et
#             if os.path.exists(speech_file):
#                 pygame.mixer.music.load(speech_file)
#                 pygame.mixer.music.play()
#                 while pygame.mixer.music.get_busy():
#                     time.sleep(0.1)
#                 pygame.mixer.music.unload() # Dosyayı serbest bırak
#             else:
#                 print(f"HATA: {speech_file} oluşturulamadı. Piper yüklü mü?")

#         except Exception as e:
#             print(f"Ses çalma hatası: {e}")
#         finally:
#             self.is_speaking = False

#     def _piper_tts(self, text, output_file):
#         # Modelin tam adını kontrol et (tr_TR-medium.onnx mi yoksa başka mı?)
#         model_path = "tr_TR-medium.onnx" 
        
#         if not os.path.exists(model_path):
#             print(f"HATA: Ses modeli ({model_path}) bulunamadı! Dosya src klasöründe mi?")
#             return

#         # Windows'ta Piper bazen tırnak işaretleri yüzünden takılabilir
#         # Echo yerine doğrudan metni göndermeyi deneyelim
#         print(f"Piper çalışıyor: '{text}' seslendiriliyor...")
#         command = f'echo {text} | piper --model {model_path} --output_file {output_file}'
        
#         exit_code = os.system(command)
#         if exit_code != 0:
#             print(f"Piper komutu başarısız oldu! Hata kodu: {exit_code}")



