import cv2
import pytesseract
import numpy as np
import logging
from core.hardware_check import HardwareDetector

class OCREngine:
    """
    Mesin utama untuk memproses gambar dan mengekstraksi teks.
    Dilengkapi dengan teknik preprocessing untuk meningkatkan akurasi pada latar belakang kompleks.
    """
    def __init__(self):
        self.detector = HardwareDetector()
        self.hardware_info = self.detector.get_optimal_execution_provider()
        logging.info(f"OCREngine diinisialisasi menggunakan: {self.hardware_info['hardware']}")
    
    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        if img is None: return None

        h, w = img.shape[:2]
        # KITA PERKETAT LAGI: Ambil hanya 10% area terbawah (tadinya 15-20%)
        # Ini akan membuang teks sampah/ranting di bagian atas watermark
        roi = img[int(h*0.90):h, 0:w] 

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Perbesar 2x agar teks lebih jelas
        gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

        # Thresholding Inverted
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Pastikan file debug disimpan di folder root agar mudah ditemukan
        # Kita gunakan os.path untuk memastikan lokasi penyimpanan
        import os
        debug_path = os.path.join(os.getcwd(), "debug_ocr.png")
        # Thresholding Inverted
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # TAMBAHKAN INI: Menebalkan teks sedikit agar angka 9 tidak terlihat seperti 0
        kernel = np.ones((2,2), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=1)
        cv2.imwrite(debug_path, thresh) 

        return thresh

    def extract_text(self, image_path):
        try:
            processed_img = self.preprocess_image(image_path)
            
            # Gunakan PSM 6 dan paksa Tesseract mengenali karakter koordinat
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789°\'",.NSEW/ '
            text = pytesseract.image_to_string(processed_img, config=custom_config)

            # --- PEMBERSIHAN KHUSUS HALUSINASI ---
            # 1. Ubah halusinasi '7/' atau '/64' kembali menjadi desimal ',764'
            text = text.replace('7/', ',').replace('/', ',')
            
            # 2. Hapus semua spasi agar angka yang terpisah (seperti 43 764) menyatu kembali
            text = text.replace(" ", "")
            
            return text
        except Exception as e:
            logging.error(f"Terjadi kesalahan saat OCR: {e}")
            return ""
        
# --- BLOK PENGUJIAN LOKAL ---
if __name__ == "__main__":
    # Ganti dengan salah satu path foto sampel Anda untuk testing
    # sample_path = "path/to/your/photo.jpg"
    # engine = OCREngine()
    # print(engine.extract_text(sample_path))
    pass