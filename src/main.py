import cv2
import time
import os
# Importu daha güvenli hale getirdik
from vision import VisionSystem 
from audio import AudioSystem
CEVIRI_SOZLUGU = {
    "person": "kişi", "car": "araba", "motorcycle": "motor",
    "bus": "otobüs", "truck": "kamyon", "traffic light": "trafik lambası",
    "stop sign": "dur tabelası", "dog": "köpek", "cat": "kedi",
    "cell phone": "telefon", "cup": "bardak", "chair": "sandalye",
    "bicycle": "bisiklet"
}

def start_glasses():
    print("\n[ADIM 1] Sistem bileşenleri başlatılıyor...")
    
    try:
        # Sınıfı doğrudan çağırıyoruz
        vision = VisionSystem()
        audio = AudioSystem()
        print("[ADIM 2] Modeller ve Ses hazır.")
    except Exception as e:
        print(f"[HATA] Başlatma hatası: {e}")
        return

    print("[ADIM 3] Kamera açılıyor...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[HATA] Kamera bulunamadı veya meşgul!")
        return

    # Nesne takip sözlüğü
    last_seen = {} 
    
    # Pencereyi zorla oluştur ve en üstte tut
    cv2.namedWindow("Smart Glasses v1.0", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Smart Glasses v1.0", cv2.WND_PROP_TOPMOST, 1)

    print("\n--- SİSTEM ÇALIŞIYOR ---")
    print("Çıkmak için kamera penceresindeyken 'q' tuşuna basın.\n")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Görüntü alınamadı.")
            break

        # Görüntüyü işle ve nesneleri al
        annotated_frame, objects = vision.detect(frame)
        current_time = time.time()

        if objects:
            current_objects = set(objects)
            to_speak = []

            for obj in current_objects:
                # 5 saniye kuralı
                if obj not in last_seen or (current_time - last_seen[obj] > 5):
                    to_speak.append(obj)
                    last_seen[obj] = current_time
            # Döngü içindeki çeviri kısmını şöyle değiştir:
            if to_speak:
                # Sözlükte kelimenin Türkçesi varsa al, yoksa İngilizcesini (obj) bırak
                translated_objects = [CEVIRI_SOZLUGU.get(obj, obj) for obj in to_speak]
                
                obj_text = ", ".join(translated_objects)
                print(f"[MANTIK] Seslendiriliyor: {obj_text}")
                audio.speak(f"Önünüzde {obj_text} var.")

        # --- EKSİK OLAN VE PENCEREYİ AÇAN KISIM BURASI ---
        cv2.imshow("Smart Glasses v1.0", annotated_frame)
        
        # 'q' tuşuna basılırsa çık (Bu satır olmazsa pencere donar)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\nSistem kapatıldı.")

if __name__ == "__main__":
    start_glasses()