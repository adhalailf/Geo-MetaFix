import re
import logging

class GeoParser:
    def __init__(self):
        # Regex ini hanya fokus mencari angka-angka sebelum huruf arah
        # Kelompok 1: Derajat, Kelompok 2: Menit, Kelompok 3: Detik (desimal), Kelompok 4: Arah
        self.coord_pattern = r"(\d{1,3})[^\dNSEW]?(\d{2})[^\dNSEW]?(\d{2}(?:[.,]\d+)?)[^\dNSEW]*([NSEW])"
        
        self.date_pattern = r"(\d{1,2})[a-zA-Z]+(\d{4})"
        self.time_pattern = r"(\d{2})[:.](\d{2})[:.](\d{2})"

    def dms_to_decimal(self, degrees, minutes, seconds, direction):
        try:
            # Ganti koma desimal menjadi titik agar bisa dihitung
            seconds = float(str(seconds).replace(',', '.'))
            dd = float(degrees) + float(minutes)/60 + seconds/3600
            if direction in ['S', 'W']:
                dd *= -1
            return round(dd, 6)
        except:
            return None

    def parse_text(self, raw_text):
        results = {"lat": None, "lon": None, "timestamp": None, "is_valid": False}
        
        # Bersihkan teks dari sampah visual sebelum diproses
        clean_text = raw_text.upper()

        # Cari koordinat
        matches = re.findall(self.coord_pattern, clean_text)
        
        for m in matches:
            deg, minute, sec, direction = m
            val = self.dms_to_decimal(deg, minute, sec, direction)
            
            if direction in ['N', 'S']:
                results["lat"] = val
            elif direction in ['E', 'W']:
                results["lon"] = val

        # Parsing Timestamp (Manual agar lebih akurat)
        time_match = re.search(r"(\d{2})[:.](\d{2})[:.](\d{2})", clean_text)
        if time_match:
            # Kita asumsikan tanggal dari nama file atau teks jika ada
            # Untuk sementara kita ambil jamnya dulu agar valid
            results["timestamp"] = f"2025:09:27 {time_match.group(1)}:{time_match.group(2)}:{time_match.group(3)}"

        if results["lat"] is not None and results["lon"] is not None:
            results["is_valid"] = True
            
        return results