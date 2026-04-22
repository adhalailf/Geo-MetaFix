import subprocess
import platform
import logging

# Konfigurasi logging dasar untuk mencatat aktivitas sistem
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class HardwareDetector:
    """
    Kelas untuk mendeteksi ketersediaan GPU (NVIDIA/AMD) pada sistem pengguna.
    Ini menentukan apakah Geo-MetaFix akan menggunakan CPU atau Akselerasi GPU.
    """
    def __init__(self):
        self.os_type = platform.system()

    def check_nvidia(self):
        """Mendeteksi GPU NVIDIA melalui command nvidia-smi."""
        try:
            # Gunakan flag agar tidak memunculkan jendela CMD yang mengganggu di Windows
            startupinfo = None
            if self.os_type == 'Windows':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            subprocess.check_output(['nvidia-smi'], startupinfo=startupinfo)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def check_amd_windows(self):
        """Mendeteksi GPU AMD khusus di environment Windows via WMIC."""
        if self.os_type != "Windows":
            return False
        
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            output = subprocess.check_output(
                ['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                startupinfo=startupinfo
            ).decode('utf-8', errors='ignore')
            
            if "AMD" in output or "Radeon" in output:
                return True
        except Exception as e:
            logging.debug(f"Pengecekan AMD gagal: {e}")
            
        return False
    
    def check_mac_gpu(self):
        """Mendeteksi GPU pada macOS (Intel atau Apple Silicon)."""
        if self.os_type != "Darwin": # Darwin adalah nama sistem kernel macOS
            return False
        
        try:
            # Menggunakan system_profiler untuk cek hardware grafis
            output = subprocess.check_output(['system_profiler', 'SPDisplaysDataType']).decode('utf-8')
            if "Chipset Model" in output:
                return True
        except Exception:
            return False
        return False
    

    def get_optimal_execution_provider(self):
        """
        Mengembalikan jenis Provider yang optimal untuk ONNX Runtime 
        berdasarkan deteksi hardware.
        """
        logging.info("Memindai perangkat keras sistem...")

        if self.os_type == "Darwin":
            logging.info("Sistem macOS terdeteksi. Menggunakan CoreML/CPU Backend.")
            return {
                "status": "STANDARD/MAC",
                "hardware": "Apple Hardware",
                "onnx_provider": "CoreMLExecutionProvider" # Jika tersedia
            }
        
        if self.check_nvidia():
            logging.info("GPU NVIDIA terdeteksi!")
            return {
                "status": "ACCELERATED",
                "hardware": "NVIDIA",
                "onnx_provider": "CUDAExecutionProvider"
            }
            
        if self.check_amd_windows():
            logging.info("GPU AMD Radeon terdeteksi!")
            return {
                "status": "ACCELERATED",
                "hardware": "AMD",
                "onnx_provider": "DmlExecutionProvider" # DirectML untuk Windows
            }

        logging.info("Tidak ada GPU diskrit yang terdeteksi. Menggunakan mode Standar.")
        return {
            "status": "STANDARD",
            "hardware": "CPU",
            "onnx_provider": "CPUExecutionProvider"
        }

# Blok pengujian (Hanya berjalan jika file ini dieksekusi langsung)
if __name__ == "__main__":
    print("--- Geo-MetaFix Hardware Diagnostic ---")
    detector = HardwareDetector()
    result = detector.get_optimal_execution_provider()
    
    print("\n[Hasil Deteksi]")
    print(f"Mode Mesin    : {result['status']}")
    print(f"Perangkat     : {result['hardware']}")
    print(f"ONNX Provider : {result['onnx_provider']}")