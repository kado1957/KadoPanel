# -*- coding: utf-8 -*-

import os
from .detector import ImageDetector

class SystemInfo:
    def get_free_mb(self, path):
        try:
            st = os.statvfs(path)
            return int((st.f_bavail * st.f_frsize) / 1024 / 1024)
        except Exception:
            return 0

    def get_meminfo(self):
        result = {"mem_total_mb": 0, "mem_free_mb": 0}
        try:
            for line in open("/proc/meminfo"):
                if line.startswith("MemTotal:"):
                    result["mem_total_mb"] = int(line.split()[1]) // 1024
                elif line.startswith("MemAvailable:"):
                    result["mem_free_mb"] = int(line.split()[1]) // 1024
        except Exception:
            pass
        return result

    def get_all(self):
        detector = ImageDetector().detect()
        mem = self.get_meminfo()
        return {
            "receiver": detector.get("model", "Unknown"),
            "image": detector.get("image", "Unknown"),
            "python": detector.get("python", "Unknown"),
            "machine": detector.get("machine", "Unknown"),
            "flash_free_mb": self.get_free_mb("/"),
            "tmp_free_mb": self.get_free_mb("/tmp"),
            "mem_total_mb": mem["mem_total_mb"],
            "mem_free_mb": mem["mem_free_mb"],
        }
