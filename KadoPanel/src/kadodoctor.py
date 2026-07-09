# -*- coding: utf-8 -*-

import os
from .config import CRASH_REPORT_FILE
from .logger import Logger

class KadoDoctor:
    CRASH_DIRS = ["/home/root/logs", "/media/hdd", "/tmp"]

    def find_latest_crash(self):
        candidates = []
        for folder in self.CRASH_DIRS:
            if not os.path.exists(folder):
                continue
            try:
                for name in os.listdir(folder):
                    low = name.lower()
                    if ("crash" in low and (low.endswith(".log") or low.endswith(".txt"))) or low.startswith("enigma2_crash"):
                        full = os.path.join(folder, name)
                        candidates.append((os.path.getmtime(full), full))
            except Exception:
                pass
        if not candidates:
            return ""
        candidates.sort(reverse=True)
        return candidates[0][1]

    def analyze_text(self, text):
        rules = [
            ("ModuleNotFoundError", "Missing Python module. Install the required dependency or remove the plugin causing it."),
            ("ImportError", "Plugin dependency problem. Check the plugin and required libraries."),
            ("skin.SkinError", "Skin compatibility issue. Switch to default skin or remove the last skin installed."),
            ("No space left on device", "Flash is full. Clean temporary files or remove unused plugins."),
            ("Segmentation fault", "Native binary crash. Check emu/plugin compatibility with your image."),
            ("Traceback", "Python exception detected. Check the last plugin shown in the traceback."),
        ]
        findings = []
        for key, advice in rules:
            if key.lower() in text.lower():
                findings.append((key, advice))
        return findings

    def inspect_latest(self):
        latest = self.find_latest_crash()
        if not latest:
            return {"latest_crash": "", "findings": [], "report": "No crash log found."}
        try:
            data = open(latest, "r", errors="ignore").read()[-12000:]
        except TypeError:
            data = open(latest, "r").read()[-12000:]
        findings = self.analyze_text(data)
        lines = ["Kado Doctor Crash Report", "=" * 32, "Latest crash: %s" % latest, ""]
        if findings:
            for key, advice in findings:
                lines.append("Detected: %s" % key)
                lines.append("Advice: %s" % advice)
                lines.append("")
        else:
            lines.append("No known pattern detected yet.")
            lines.append("Send the crash log for deeper analysis.")
        try:
            open(CRASH_REPORT_FILE, "w").write("\n".join(lines))
            Logger.write("Crash report created: %s" % CRASH_REPORT_FILE)
        except Exception:
            pass
        return {"latest_crash": latest, "findings": findings, "report": "\n".join(lines)}
