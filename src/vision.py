import os
from ultralytics import YOLO

class VisionSystem:
    def __init__(self, model_name="yolo11n_float32.tflite"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.full_model_path = os.path.join(current_dir, "..", "models", model_name)
        
        print(f"[VİZYON] Model yükleniyor: {self.full_model_path}")
        self.model = YOLO(self.full_model_path, task="detect")
        
        # Etiketleri modelin içinden otomatik alıyoruz
        self.names = self.model.names 

    def detect(self, frame):
        # conf=0.45 güven değeri, imgsz=320 hız içindir
        results = self.model.predict(frame, conf=0.45, imgsz=320, verbose=False)
        
        detected_objects = []
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.names.get(cls_id, f"Nesne-{cls_id}")
                detected_objects.append(label)
        
        return results[0].plot(), detected_objects