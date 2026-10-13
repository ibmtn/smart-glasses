# Üçüncü taraf bileşenler

`LICENSE` dosyasındaki MIT lisansı yalnızca bu depodaki **kendi yazdığım kaynak kodu** kapsar
(`src/`, `scripts/`, `export.py`).

Aşağıdaki dosyalar MIT kapsamında **değildir**; kendi lisanslarına tabidir:

| Dosya | Sahibi | Lisans |
|---|---|---|
| `yolo11n.pt`, `yolo11n.onnx` | Ultralytics | AGPL-3.0 |
| `models/yolo11n_float32.tflite`, `models/yolo11n_saved_model/` | Ultralytics (YOLO11n'den dönüştürüldü) | AGPL-3.0 |
| `calibration_image_sample_data_20x128x128x3_float32.npy` | Model dönüştürme sırasında üretilen örnek veri | AGPL-3.0 (modelle birlikte) |

Proje çalışırken şu kütüphaneleri kullanır; bunlar depoya dahil değildir ve kendi lisanslarıyla kurulur:

- [Ultralytics](https://github.com/ultralytics/ultralytics) — AGPL-3.0. Bu kütüphaneyle birlikte dağıtılan veya ağ üzerinden sunulan bir bütün, AGPL-3.0 koşullarına uymalıdır.
- [OpenCV](https://github.com/opencv/opencv) — Apache-2.0
- [Google Cloud Text-to-Speech istemcisi](https://github.com/googleapis/google-cloud-python) — Apache-2.0
- [pygame](https://github.com/pygame/pygame) — LGPL-2.1

Ayrıntılar: https://www.ultralytics.com/license
