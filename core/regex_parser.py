import re
import logging
from datetime import datetime

class GeoParser:
    """
    Bertugas membedah teks mentah hasil OCR menjadi data terstruktur:
    Latitude, Longitude, dan Timestamp.
    """

    def __init__(self):
        # Pola Regex untuk DMS (Degree Minute Second)
        # Mendukung angka desimal dengan titik (.) atau koma (,)
        # Contoh: 2°39'32,796"N atau 117°21'49.926"E
        self.coord_pattern = r"(\d{1,3})°(\d{1,2})'(\d{1,2}(?:[.,]\d+)?)\"([NSEW])"
        
        # Pola Regex untuk Tanggal (Contoh: 24 Sep 2025 atau 18 Agustus 2025)
        self.date_pattern = r"(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})"
        
        # Pola Regex untuk Waktu (Contoh: 12.39.16 atau 10:08:37)
        self.time_pattern = r"(\d{2})[:.](\d{2})[:.](\d{2})"

    def dms_to_decimal(self, degrees, minutes, seconds, direction):
        """Mengonversi format DMS ke Decimal Degrees untuk standar EXIF GPS."""
        # Ganti koma ke titik untuk kalkulasi float
        seconds = float(seconds.replace(',', '.'))
        decimal = float(degrees) + float(minutes)/60 + seconds/3600
        
        if direction in ['S', 'W']:
            decimal *= -1
        return round(decimal, 6)

    def parse_text(self, raw_text):
        """
        Fungsi utama untuk mengekstraksi semua data dari string mentah.
        """
        results = {
            "lat": None,
            "lon": None,
            "timestamp": None,
            "is_valid": False
        }

        # 1. Cari Koordinat (Biasanya ada dua: Lat dan Lon)
        coords = re.findall(self.coord_pattern, raw_text)
        if len(coords) >= 2:
            results["lat"] = self.dms_to_decimal(*coords[0])
            results["lon"] = self.dms_to_decimal(*coords[1])
        
        # 2. Cari Tanggal & Waktu
        date_match = re.search(self.date_pattern, raw_text)
        time_match = re.search(self.time_pattern, raw_text)
        
        if date_match and time_match:
            # Sederhanakan format waktu ke standar EXIF YYYY:MM:DD HH:MM:SS
            # Catatan: Diperlukan pemetaan nama bulan jika ingin lebih presisi
            results["timestamp"] = f"{date_match.group(3)}:{date_match.group(2)}:{date_match.group(1)} {time_match.group(0)}"

        # Validasi akhir: Jika koordinat lengkap, anggap valid
        if results["lat"] is not None and results["lon"] is not None:
            results["is_valid"] = True
            
        return results

# --- BLOK PENGUJIAN MANUAL ---
if __name__ == "__main__":
    parser = GeoParser()
    
    # Simulasi hasil OCR dari image_0.png Anda
    sample_ocr_result = """
    24 Sep 2025 12.39.16
    2°39'32,796"N 117°21'49,926"E
    """
    
    data = parser.parse_text(sample_ocr_result)
    
    print("--- Testing Regex Parser ---")
    print(f"Raw Text: {sample_ocr_result.strip()}")
    print("-" * 30)
    if data["is_valid"]:
        print(f"Hasil Latitude  : {data['lat']}")
        print(f"Hasil Longitude : {data['lon']}")
        print(f"Timestamp       : {data['timestamp']}")
    else:
        print("Peringatan: Data koordinat tidak lengkap/tidak terbaca!")