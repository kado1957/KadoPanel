# -*- coding: utf-8 -*-

import os
import platform

class ImageDetector:
    def _read_first_existing(self, paths):
        for path in paths:
            try:
                if os.path.exists(path):
                    return open(path, "r").read()
            except Exception:
                pass
        return ""

    def detect_image(self):
        data = self._read_first_existing([
            "/etc/issue", "/etc/image-version", "/etc/openbh-release",
            "/etc/openatv-release", "/etc/openvix-release", "/etc/egami-version"
        ]).lower()
        if "black hole" in data or "openbh" in data:
            return "OpenBH"
        if "openvix" in data:
            return "OpenViX"
        if "openatv" in data:
            return "OpenATV"
        if "egami" in data:
            return "Egami"
        if "openpli" in data:
            return "OpenPLi"
        if "pure2" in data:
            return "PurE2"
        return "Unknown"

    def detect_model(self):
        for p in ["/proc/stb/info/model", "/proc/stb/info/boxtype"]:
            try:
                if os.path.exists(p):
                    return open(p).read().strip()
            except Exception:
                pass
        return "Unknown"

    def detect(self):
        return {
            "image": self.detect_image(),
            "model": self.detect_model(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "system": platform.system()
        }
