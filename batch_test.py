import os
import logging
from core.ocr_engine import OCREngine
from core.regex_parser import GeoParser

# Matikan log default agar tampilan terminal lebih rapi
logging.getLogger().setLevel(logging.ERROR)

def run_batch_test(directory_path):
    print(f"\n{'='*50}")
    print(f"MEMULAI UJI COBA MASSAL")
    print(f"Folder: {directory_path}")
    print(f"{'='*50}\n")

    engine = OCREngine()
    parser = GeoParser()

    # Cari semua file gambar (jpg, jpeg, png) dan abaikan file debug
    valid_extensions = ('.jpg', '.jpeg', '.png')
    image_files = [f for f in os.listdir(directory_path) 
                   if f.lower().endswith(valid_extensions) and f != "debug_ocr.png"]

    if not image_files:
        print("[-] Tidak ada foto ditemukan di folder tersebut.")
        return

    total_files = len(image_files)
    success_count = 0
    failed_files = []

    for index, img_name in enumerate(image_files, 1):
        img_path = os.path.join(directory_path, img_name)
        print(f"[{index}/{total_files}] Memproses {img_name}...", end=" ")
        
        raw_text = engine.extract_text(img_path)
        data = parser.parse_text(raw_text)

        if data["is_valid"]:
            print("✅ VALID")
            success_count += 1
        else:
            print("❌ GAGAL")
            # Simpan data yang gagal untuk dianalisis nanti
            failed_files.append({
                "file": img_name,
                "raw_text": raw_text.replace('\n', ' ') # Gabungkan baris agar rapi di terminal
            })

    # --- CETAK RAPOR AKHIR ---
    print(f"\n{'='*50}")
    print("RAPOR UJI COBA MASSAL")
    print(f"{'='*50}")
    print(f"Total Foto   : {total_files}")
    print(f"Berhasil     : {success_count}")
    print(f"Gagal        : {total_files - success_count}")
    print(f"Akurasi      : {round((success_count/total_files)*100, 2)}%")

    # Jika ada yang gagal, tampilkan teks mentahnya agar kita tahu penyakitnya
    if failed_files:
        print("\n--- DAFTAR FOTO YANG GAGAL ---")
        for fail in failed_files:
            print(f"\nFile: {fail['file']}")
            print(f"Teks Mentah OCR: '{fail['raw_text']}'")

if __name__ == "__main__":
    # Tentukan folder tempat Anda menyimpan foto-foto sampel
    # Gunakan "." jika foto ada di folder yang sama dengan skrip ini
    FOLDER_FOTO = "./assets/images" 
    
    run_batch_test(FOLDER_FOTO)