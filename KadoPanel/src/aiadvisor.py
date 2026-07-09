# -*- coding: utf-8 -*-

class AIAdvisor:
    def advise(self, health_result, neoboot=None, doctor=None):
        advice = []

        if health_result.get("ready"):
            advice.append("System Ready. You can continue safely.")

        for name, ok, value in health_result.get("checks", []):
            if ok:
                continue
            if name == "Image":
                advice.append("Image is not fully supported yet. Use Safe Mode only.")
            elif name == "Python 3":
                advice.append("Python 3 is required for Kado Panel.")
            elif name == "Flash":
                advice.append("Flash space is low. Clean temporary files or remove unused plugins.")
            elif name == "RAM":
                advice.append("RAM is low. Restart Enigma2 before installing packages.")
            elif name == "TMP":
                advice.append("/tmp space is low. Clean temporary files.")
            elif name == "Internet":
                advice.append("Internet is not connected. Check network settings before updates.")
            else:
                advice.append("%s needs attention: %s" % (name, value))

        if neoboot and neoboot.get("installed"):
            advice.append("NeoBoot detected. Be careful when syncing settings between images.")

        if doctor and doctor.get("latest_crash"):
            advice.append("Crash log found. Use Kado Doctor to inspect possible causes.")

        return "\n".join(advice) if advice else "Safe Mode recommended."
