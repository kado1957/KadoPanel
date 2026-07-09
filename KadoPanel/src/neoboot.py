# -*- coding: utf-8 -*-

import os

class NeoBootManager:
    def detect(self):
        possible_paths = [
            "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot",
            "/media/hdd/ImagesUpload",
            "/media/usb/ImagesUpload"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return {"installed": True, "path": path, "version": "9.65 target"}
        return {"installed": False, "path": "", "version": ""}
