import unittest
import sys
import os

# Menambahkan path folder root agar bisa mengimport dari folder core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.regex_parser import GeoParser

class TestGeoParser(unittest.TestCase):
    def setUp(self):
        self.parser = GeoParser()

    def test_standard_dms_comma(self):
        """Uji format DMS dengan koma (sampel image_0)"""
        raw = "24 Sep 2025 12.39.16 2°39'32,796\"N 117°21'49,926\"E"
        res = self.parser.parse_text(raw)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["lat"], 2.65911)
        self.assertEqual(res["timestamp"], "2025:09:24 12:39:16")

    def test_indonesian_month_full(self):
        """Uji format bulan Indonesia lengkap (sampel image_2)"""
        raw = "18 Agustus 2025 2°40'7,524\"N 117°22'23,898\"E"
        res = self.parser.parse_text(raw)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["lat"], 2.668757)
        self.assertEqual(res["timestamp"][:10], "2025:08:18")

    def test_missing_coordinates(self):
        """Uji jika koordinat tidak ada (kasus error yang kita inginkan)"""
        raw = "18 Agu 2025 Foto tanpa koordinat di sini"
        res = self.parser.parse_text(raw)
        self.assertFalse(res["is_valid"])
        self.assertIsNone(res["lat"])

if __name__ == "__main__":
    unittest.main()