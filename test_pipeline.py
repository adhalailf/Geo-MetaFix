import os
import logging
from core.ocr_engine import OCREngine
from core.regex_parser import GeoParser

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_full_pipeline(image_path):
    print(f"\n{'='*50}")
    print(f"Memproses: {os.path.basename(image_path)}")
    print(f"{'='*50}")

    # 1. Inisialisasi Engine
    engine = OCREngine()
    parser = GeoParser()

    # 2. Ekstraksi Teks (Mata)
    print("[1/3] Menjalankan OCR...")
    raw_text = engine.extract_text(image_path)
    
    if not raw_text.strip():
        print("[-] Gagal mengekstraksi teks dari gambar.")
        return

    print(f"[+] Teks Mentah Ditemukan:\n{raw_text.strip()}")
    print("-" * 30)

    # 3. Parsing Data (Otak)
    print("[2/3] Membedah koordinat...")
    data = parser.parse_text(raw_text)

    # 4. Hasil Akhir (Integrasi)
    print("[3/3] Hasil Akhir:")
    if data["is_valid"]:
        print(f"      ✅ Status     : VALID")
        print(f"      📍 Latitude   : {data['lat']}")
        print(f"      📍 Longitude  : {data['lon']}")
        print(f"      📅 Timestamp  : {data['timestamp']}")
    else:
        print(f"      ⚠️ Status     : DATA TIDAK LENGKAP")
        print(f"      Pesan: Koordinat tidak ditemukan dalam teks mentah.")
    
    print(f"{'='*50}\n")

if __name__ == "__main__":
    # Masukkan path salah satu foto asli Anda di sini
    # Contoh untuk macOS/Linux: "images/f_TimePhoto_20250924_123916.jpg"
    path_foto = "f_TimePhoto_20250927_153916.jpg" # Pastikan file ada di folder yang sama atau tulis path lengkap
    
    if os.path.exists(path_foto):
        run_full_pipeline(path_foto)
    else:
        print(f"Error: File {path_foto} tidak ditemukan. Pastikan path sudah benar.")