import time

import cv2

from audio import AudioSystem
from vision import VisionSystem

WINDOW_NAME = "Smart Glasses v1.0"
REPEAT_AFTER_SECONDS = 5  # Aynı nesne bu süre dolmadan tekrar söylenmez

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
        vision = VisionSystem()
        audio = AudioSystem()
        print("[ADIM 2] Modeller ve ses hazır.")
    except Exception as e:
        print(f"[HATA] Başlatma hatası: {e}")
        return

    print("[ADIM 3] Kamera açılıyor...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[HATA] Kamera bulunamadı veya meşgul!")
        return

    # Nesne -> en son seslendirildiği zaman
    last_spoken = {}

    # Pencereyi oluştur ve en üstte tut
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_TOPMOST, 1)

    print("\n--- SİSTEM ÇALIŞIYOR ---")
    print("Çıkmak için kamera penceresindeyken 'q' tuşuna basın.\n")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Görüntü alınamadı.")
                break

            annotated_frame, objects = vision.detect(frame)
            now = time.time()

            to_speak = [
                obj for obj in set(objects)
                if now - last_spoken.get(obj, 0) > REPEAT_AFTER_SECONDS
            ]
            if to_speak:
                # Sözlükte Türkçesi varsa onu, yoksa modelin verdiği adı kullan
                obj_text = ", ".join(CEVIRI_SOZLUGU.get(obj, obj) for obj in to_speak)
                # Ses meşgulken atlanan nesneler "söylendi" sayılmaz; bir sonraki karede tekrar denenir
                if audio.speak(f"Önünüzde {obj_text} var."):
                    print(f"[MANTIK] Seslendiriliyor: {obj_text}")
                    for obj in to_speak:
                        last_spoken[obj] = now

            cv2.imshow(WINDOW_NAME, annotated_frame)

            # waitKey olmadan pencere donar; 'q' ile çıkılır
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("\nSistem kapatıldı.")


if __name__ == "__main__":
    start_glasses()
