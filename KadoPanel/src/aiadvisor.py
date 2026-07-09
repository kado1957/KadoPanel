# -*- coding: utf-8 -*-

class AIAdvisor:
    def advise(self, health_result):
        if health_result.get("ready"):
            return "System Ready. You can continue safely."

        advice = []
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
            else:
                advice.append("%s needs attention: %s" % (name, value))
        return "\n".join(advice) if advice else "Safe Mode recommended."
