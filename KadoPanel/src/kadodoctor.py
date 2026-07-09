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

    def inspect_latest(self):
        latest = self.find_latest_crash()
        if not latest:
            return {"latest_crash": "", "findings": [], "report": "No crash log found."}
        try:
            data = open(latest, "r", errors="ignore").read()[-12000:]
        except TypeError:
            data = open(latest, "r").read()[-12000:]
        rules = [("ModuleNotFoundError", "Missing Python module."), ("ImportError", "Plugin dependency problem."), ("skin.SkinError", "Skin compatibility issue."), ("No space left on device", "Flash is full."), ("Segmentation fault", "Native binary crash."), ("Traceback", "Python exception detected.")]
        findings = [(k, a) for k, a in rules if k.lower() in data.lower()]
        lines = ["Kado Doctor Crash Report", "=" * 32, "Latest crash: %s" % latest, ""]
        if findings:
            for key, advice in findings:
                lines.append("Detected: %s" % key)
                lines.append("Advice: %s" % advice)
                lines.append("")
        else:
            lines.append("No known pattern detected yet.")
        try:
            open(CRASH_REPORT_FILE, "w").write("\n".join(lines))
            Logger.write("Crash report created: %s" % CRASH_REPORT_FILE)
        except Exception:
            pass
        return {"latest_crash": latest, "findings": findings, "report": "\n".join(lines)}
