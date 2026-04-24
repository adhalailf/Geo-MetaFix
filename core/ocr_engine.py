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
        # 1. ROI Fokus
        roi = img[int(h*0.92):h, int(w*0.435):w] 

        # 2. Grayscale & Contrast
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0) 

        # 3. Upscale (3x agar angka lebih besar dan jelas)
        gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

        # 4. Blur sedikit untuk menyatukan pixel yang pecah
        gray = cv2.GaussianBlur(gray, (3,3), 0)

        # 5. Threshold (Putih jadi Hitam, Hitam jadi Putih)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # 6. Tebalkan Teks Hitam (Gunakan Erode karena background putih)
        kernel = np.ones((2,2), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=1)

        # Simpan untuk cek visual
        import os
        cv2.imwrite(os.path.join(os.getcwd(), "debug_ocr.png"), thresh) 

        return thresh

   
    def extract_text(self, image_path):
        try:
            processed_img = self.preprocess_image(image_path)
            
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(processed_img, config=custom_config)
            text = text.replace('7/', ',').replace('/', ',').strip()

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