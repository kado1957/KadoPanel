# -*- coding: utf-8 -*-

class AIAdvisor:
    def advise(self, health_result, neoboot=None, doctor=None, update=None, installer=None):
        advice = []

        if health_result.get("ready"):
            advice.append("System Ready. You can continue safely.")

        for name, ok, value in health_result.get("checks", []):
            if ok:
                continue
            if name == "Backup Storage":
                advice.append("Backup storage is not ready. Mount SSD/HDD as /media/hdd before creating backup.")
            elif name == "Image":
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

        if neoboot and neoboot.get("installed"):
            advice.append("NeoBoot detected. Always create a backup before syncing settings between images.")

        if doctor and doctor.get("latest_crash"):
            advice.append("Crash log found. Use Kado Doctor to inspect possible causes.")

        if update:
            if update.get("update_available"):
                advice.append("New Kado Panel version available: %s" % update.get("remote_version"))
            elif update.get("ok"):
                advice.append("Kado Panel is up to date.")

        if installer:
            advice.append("Compatible plugins detected: %s" % installer.get("count", 0))
            advice.append("Installer is still in safe preview mode.")

        return "\n".join(advice) if advice else "Safe Mode recommended."
