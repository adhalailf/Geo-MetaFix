import re
import logging

class GeoParser:
    def __init__(self):
        # Pattern yang toleran terhadap simbol yang hilang atau salah baca
        # Group: 1.Derajat, 2.Menit, 3.Detik, 4.Arah
        self.coord_pattern = r"(\d{1,3})[^\dNSEW]+(\d{1,2})[^\dNSEW]+(\d{1,2}[.,]\d+)[^\dNSEW]*([NSEW])"
        
        self.date_pattern = r"(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})"
        self.time_pattern = r"(\d{2})[:.](\d{2})[:.](\d{2})"
        self.month_map = { 'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'mei': '05', 'jun': '06', 
                           'jul': '07', 'agu': '08', 'sep': '09', 'okt': '10', 'nov': '11', 'des': '12' }

    def dms_to_decimal(self, degrees, minutes, seconds, direction):
        try:
            # 1. Hapus semua karakter yang BUKAN angka, titik, atau koma
            # Ini akan membuang tanda petik (') atau (") yang ikut terbawa
            import re
            clean_seconds = re.sub(r"[^\d.,]", "", str(seconds))
            
            # 2. Normalisasi koma menjadi titik untuk kalkulasi float
            clean_seconds = clean_seconds.replace(',', '.')
            
            # 3. Hitung desimal
            dd = float(degrees) + float(minutes)/60 + float(clean_seconds)/3600
            
            if direction in ['S', 'W']:
                dd *= -1
            return round(dd, 6)
        except Exception as e:
            logging.error(f"Gagal konversi DMS: {seconds} -> {e}")
            return None

    def parse_text(self, raw_text):
        results = {"lat": None, "lon": None, "timestamp": None, "is_valid": False}
        
        # 1. Parsing Koordinat
        # Kita cari semua yang cocok dengan pola DMS
        potential_coords = re.findall(self.coord_pattern, raw_text)
        
        for deg, minute, sec, direction in potential_coords:
            # Validasi Dasar: Derajat tidak boleh lebih dari 180 (membuang angka tahun seperti 2025)
            if int(deg) > 180:
                continue
                
            val = self.dms_to_decimal(deg, minute, sec, direction)
            if direction in ['N', 'S']:
                results["lat"] = val
            elif direction in ['E', 'W']:
                results["lon"] = val

        # 2. Parsing Tanggal & Waktu (Gunakan teks asli tanpa hapus spasi)
        date_match = re.search(self.date_pattern, raw_text)
        time_match = re.search(self.time_pattern, raw_text)
        
        if date_match and time_match:
            day = date_match.group(1).zfill(2)
            month = self.month_map.get(date_match.group(2).lower()[:3], "01")
            year = date_match.group(3)
            results["timestamp"] = f"{year}:{month}:{day} {time_match.group(0).replace('.', ':')}"

        if results["lat"] is not None and results["lon"] is not None:
            results["is_valid"] = True
            
        return results