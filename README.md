# smart-glasses

Kameradaki nesneleri YOLO11 ile gerçek zamanlı tanıyıp Türkçe sesli olarak bildiren akıllı gözlük prototipi (öğrenci projesi).

Örneğin kamerada bir kişi ve araba görünce “Önünüzde kişi, araba var.” der. Aynı nesne 5 saniye dolmadan tekrar söylenmez.

## Nasıl çalışır?

1. **Görme** (`src/vision.py`): YOLO11n modeli (TensorFlow Lite, 320 px giriş, %45 güven eşiği) kameradaki nesneleri algılar.
2. **Karar** (`src/main.py`): Algılanan nesneler Türkçeye çevrilir; yakın zamanda söylenmiş olanlar atlanır.
3. **Ses** (`src/audio.py`): Cümle Google Cloud Text-to-Speech ile Türkçe seslendirilir. Ses arka planda çalınır, görüntü donmaz.

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

### Google Cloud anahtarı

Seslendirme için bir Google Cloud servis hesabı anahtarı (JSON) gerekir. **Bu dosya depoya asla eklenmez.** İki yoldan biri:

- `GOOGLE_APPLICATION_CREDENTIALS` ortam değişkenine dosyanın yolunu verin, **ya da**
- dosyayı `credentials/google-tts.json` olarak kaydedin (bu klasör `.gitignore` ile dışarıda tutulur).

Bağlantıyı denemek için: `python scripts/tts_kontrol.py`

## Çalıştırma

```bash
python src/main.py
```

Çıkmak için kamera penceresindeyken `q` tuşuna basın.

> **Not:** TensorFlow Lite, Windows'ta yolunda Türkçe karakter (ör. `İ`, `ş`) bulunan klasördeki modeli açamaz. Projeyi `C:\Projects\smart` gibi yalnızca ASCII karakterli bir klasörde tutun.

Modeli yeniden dönüştürmek için (`yolo11n.pt` → TFLite): `pip install tensorflow` ardından `python export.py`.

## Teknolojiler

Python · OpenCV · Ultralytics YOLO11 · TensorFlow Lite · Google Cloud Text-to-Speech · pygame

## Lisans

Kaynak kodu [MIT](LICENSE) lisanslıdır. Model dosyaları Ultralytics'e aittir ve AGPL-3.0 lisanslıdır; ayrıntılar için [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
