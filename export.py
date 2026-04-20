import os
import shutil
from ultralytics import YOLO

# 1. Klasör Temizliği (Hata almamak için şart)
export_folder = "yolo11n_saved_model"
if os.path.exists(export_folder):
    shutil.rmtree(export_folder)

# 2. Modeli yükle (Dosyanın tam yerini belirleyelim)
model = YOLO("yolo11n.pt")

# 3. Export İşlemi
try:
    # Veriyi TFLite'a çeviriyoruz
    # imgsz=320 RPi için en iyisidir
    model.export(format="tflite", imgsz=320, data="coco8.yaml")
    print("\n[BAŞARILI] Model başarıyla çevrildi!")
except Exception as e:
    print(f"\n[HATA] Bir sorun oluştu: {e}")

    #export GOOGLE_APPLICATION_CREDENTIALS="/C:/smart-glasses-492614-0ff024ff67db.json/492614-0ff024ff67db.json"
    #$env:GOOGLE_APPLICATION_CREDENTIALS="C:\smart-glasses-492614-0ff02c610996\492614-0ff024ff67db.json"