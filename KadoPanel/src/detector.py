# -- coding: utf-8 --

import os
import platform


class ImageDetector(object):

    def _read_first(self, paths):
        for path in paths:
            try:
                if os.path.exists(path):
                    value = open(path, "r").read().strip()
                    if value:
                        return value
            except Exception:
                pass
        return ""

    def detect_image(self):
        files = [
            "/etc/openbh-release",
            "/etc/image-version",
            "/etc/issue",
            "/etc/os-release",
        ]

        data = ""
        for path in files:
            try:
                if os.path.exists(path):
                    data += " " + open(path, "r").read().lower()
            except Exception:
                pass

        if "openbh" in data or "open black hole" in data:
            return "OpenBH"
        if "openatv" in data:
            return "OpenATV"
        if "openvix" in data:
            return "OpenViX"
        if "openpli" in data:
            return "OpenPLi"
        if "egami" in data:
            return "Egami"
        if "pure2" in data:
            return "PurE2"

        return "Unknown"

    def detect_image_version(self):
        paths = [
            "/etc/openbh-release",
            "/etc/image-version",
            "/etc/issue",
            "/etc/os-release",
        ]

        for path in paths:
            try:
                if os.path.exists(path):
                    text = open(path, "r").read().strip().replace("\n", " ")
                    if text:
                        return text[:240]
            except Exception:
                pass

        return "Unknown"

    def detect_model(self):
        # Vu+ model file has priority.
        paths = [
            "/proc/stb/info/vumodel",
            "/proc/stb/info/boxtype",
            "/proc/stb/info/model",
            "/proc/device-tree/model",
            "/etc/hostname",
        ]

        invalid_models = {
            "",
            "unknown",
            "dm8000",
            "dreambox",
            "generic",
            "linux",
        }

        for path in paths:
            try:
                if not os.path.exists(path):
                    continue

                model = open(path, "r").read().replace("\x00", "").strip()

                if model and model.lower() not in invalid_models:
                    return model
            except Exception:
                pass

        # Fallback from image release information.
        release_paths = [
            "/etc/openbh-release",
            "/etc/image-version",
            "/etc/issue",
            "/etc/os-release",
        ]

        for path in release_paths:
            try:
                if not os.path.exists(path):
                    continue

                data = open(path, "r").read()
                lower_data = data.lower()

                known_models = [
                    "vuduo4kse",
                    "vuduo4k",
                    "vuultimo4k",
                    "vusolo4k",
                    "vuuno4kse",
                    "vuuno4k",
                    "vuzero4k",
                ]

                for model in known_models:
                    if model in lower_data:
                        return model

                for token in data.replace("\n", " ").split():
                    token = token.strip().strip('"').strip("'")
                    if token.lower().startswith("machine="):
                        value = token.split("=", 1)[1].strip()
                        if value:
                            return value
            except Exception:
                pass

        return "Unknown"

    def detect(self):
        return {
            "image": self.detect_image(),
            "image_version": self.detect_image_version(),
            "model": self.detect_model(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "system": platform.system(),
            "kernel": platform.release(),
        }
