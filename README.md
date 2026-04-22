# 🌍 Geo-MetaFix

Geo-MetaFix adalah solusi berbasis Python untuk mengembalikan integritas data geolokasi pada foto dokumentasi lapangan. Aplikasi ini secara otomatis membaca koordinat (DMS) yang tertampil visual pada foto menggunakan teknologi OCR (Optical Character Recognition) dan menyuntikkannya kembali ke dalam metadata EXIF (GPS).

Developed for professionals in mapping, forestry, and field surveying who struggle with inconsistent metadata across various smartphone brands.

---

## ✨ Fitur Utama

- ⚡ Hybrid Processing Engine: Deteksi hardware otomatis untuk mendukung akselerasi GPU (NVIDIA CUDA / AMD DirectML) atau mode CPU standar.
- 📂 Smart Batch Processing: Memproses ratusan foto dalam satu antrean dengan manajemen memori yang efisien.
- 🔍 Intelligent OCR & Regex: Ekstraksi presisi koordinat derajat-menit-detik (DMS) dan timestamp dari berbagai layout watermark.
- 🖥️ Smart Inspector Overlay: Antarmuka interaktif untuk verifikasi manual dengan fitur zoom dan koreksi data pada foto yang bermasalah.
- 🛡️ Data Integrity: Menjamin akurasi koordinat desimal hingga 6 digit di belakang koma untuk standar pemetaan profesional.

---

## 🛠️ Tech Stack

- Core: Python 3.9+
- Image Processing: OpenCV
- AI/OCR: ONNX Runtime, Tesseract OCR
- Metadata: PieXif
- GUI: PyQt6
- Data: Pandas & NumPy

---

## 🚀 Instalasi (macOS)

1. Clone Repositori
   git clone [https://github.com/adhalailf/Geo-MetaFix.git](https://github.com/adhalailf/Geo-MetaFix.git)
   cd Geo-MetaFix

2. Setup Virtual Environment
   python3 -m venv venv
   source venv/bin/activate

3. Instal Dependensi
   brew install tesseract  # Membutuhkan Homebrew
   pip install -r requirements.txt

## 📝 Roadmap
[x] Hardware Detection Logic (Hybrid Engine)
[x] Regex Coordinate Parsing
[ ] OCR Engine Implementation (ONNX/Tesseract)
[ ] GUI Development (Smart Inspector)
[ ] Final Metadata Injection Testing
Developed with integrity and precision for reliable field data. -adhalailf