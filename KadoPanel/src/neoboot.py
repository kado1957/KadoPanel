# -*- coding: utf-8 -*-

import os

class NeoBootManager:
    def detect(self):
        possible_paths = ["/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot", "/media/hdd/ImagesUpload", "/media/usb/ImagesUpload", "/media/hdd/NeoBoot", "/media/usb/NeoBoot"]
        for path in possible_paths:
            if os.path.exists(path):
                return {"installed": True, "path": path, "version": "9.65 target"}
        return {"installed": False, "path": "", "version": ""}

    def list_images(self):
        result = []
        for base in ["/media/hdd/ImagesUpload", "/media/usb/ImagesUpload", "/media/hdd/NeoBoot", "/media/usb/NeoBoot"]:
            if not os.path.exists(base):
                continue
            try:
                for item in os.listdir(base):
                    full = os.path.join(base, item)
                    if os.path.isdir(full):
                        result.append({"name": item, "path": full})
            except Exception:
                pass
        return result
