# -*- coding: utf-8 -*-

import os
import socket
from .detector import ImageDetector
from .config import REPORT_FILE
from .logger import Logger

class SystemInfo:
    def get_free_mb(self, path):
        try:
            st = os.statvfs(path)
            return int((st.f_bavail * st.f_frsize) / 1024 / 1024)
        except Exception:
            return 0

    def get_total_mb(self, path):
        try:
            st = os.statvfs(path)
            return int((st.f_blocks * st.f_frsize) / 1024 / 1024)
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

    def internet_ok(self):
        try:
            socket.create_connection(("8.8.8.8", 53), 3).close()
            return True
        except Exception:
            return False

    def get_all(self):
        detector = ImageDetector().detect()
        mem = self.get_meminfo()
        return {
            "receiver": detector.get("model", "Unknown"),
            "image": detector.get("image", "Unknown"),
            "image_version": detector.get("image_version", "Unknown"),
            "python": detector.get("python", "Unknown"),
            "machine": detector.get("machine", "Unknown"),
            "kernel": detector.get("kernel", "Unknown"),
            "enigma2": detector.get("enigma2", "Unknown"),
            "flash_total_mb": self.get_total_mb("/"),
            "flash_free_mb": self.get_free_mb("/"),
            "tmp_total_mb": self.get_total_mb("/tmp"),
            "tmp_free_mb": self.get_free_mb("/tmp"),
            "hdd_free_mb": self.get_free_mb("/media/hdd") if os.path.exists("/media/hdd") else 0,
            "usb_free_mb": self.get_free_mb("/media/usb") if os.path.exists("/media/usb") else 0,
            "mem_total_mb": mem["mem_total_mb"],
            "mem_free_mb": mem["mem_free_mb"],
            "internet": self.internet_ok(),
        }

    def create_report(self):
        info = self.get_all()
        lines = ["Kado Panel System Report", "=" * 32]
        for key in sorted(info.keys()):
            lines.append("%s: %s" % (key, info[key]))
        try:
            open(REPORT_FILE, "w").write("\n".join(lines))
            Logger.write("System report created: %s" % REPORT_FILE)
            return REPORT_FILE
        except Exception as e:
            Logger.write("System report failed: %s" % e)
            return ""
