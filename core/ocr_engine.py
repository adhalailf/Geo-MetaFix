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
        import numpy as np
        img = cv2.imread(image_path)
        if img is None: return None

        h, w = img.shape[:2]
        # Crop aman
        roi = img[int(h*0.85):h, int(w*0.02):w] 

        # 1. ISOLASI WARNA HSV (Menjaga teks tetap utuh dan solid)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 180])
        upper_white = np.array([180, 50, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)

        # 2. FILTER KONTUR (Menyapu sisa daun dari hasil HSV)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        clean_mask = np.zeros(mask.shape, dtype=np.uint8)
        
        for c in contours:
            x, y, w_box, h_box = cv2.boundingRect(c)
            area = cv2.contourArea(c)
            
            # KRITERIA DIPERLONGGAR: 
            # Menyelamatkan teks yang mungkin sedikit tersambung dengan noise
            # Buang objek sangat kecil (area < 5) dan objek sangat tinggi/besar seperti daun (h_box > 90)
            if area > 5 and h_box < 90:
                cv2.drawContours(clean_mask, [c], -1, (255), thickness=cv2.FILLED)

        # 3. Upscale & Invert (Teks hitam di atas background putih)
        clean_mask = cv2.resize(clean_mask, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        final_img = cv2.bitwise_not(clean_mask)

        # 4. Sedikit penebalan untuk OCR
        kernel = np.ones((2,2), np.uint8)
        final_img = cv2.erode(final_img, kernel, iterations=1)

        import os
        cv2.imwrite(os.path.join(os.getcwd(), "debug_ocr.png"), final_img) 
        return final_img
    

    def extract_text(self, image_path):
        try:
            processed_img = self.preprocess_image(image_path)
            
            # KUNCI PERBAIKAN: 
            # 1. Hapus parameter whitelist yang bikin error
            # 2. Kembalikan ke PSM 6 karena teks sudah bersih dan terstruktur rapi
            custom_config = r'--oem 3 --psm 6'
            
            text = pytesseract.image_to_string(processed_img, config=custom_config)

            # Sedikit pembersihan teks dari salah baca yang umum terjadi
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