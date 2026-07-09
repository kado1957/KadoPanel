# -*- coding: utf-8 -*-

from .systeminfo import SystemInfo
from .compatibility import is_supported

class HealthCheck:
    def run(self):
        info = SystemInfo().get_all()
        checks = [
            ("Receiver", True, info.get("receiver", "Unknown")),
            ("Image", is_supported(info.get("image")), "%s / %s" % (info.get("image", "Unknown"), info.get("image_version", ""))),
            ("Python 3", str(info.get("python", "0")).startswith("3"), info.get("python", "Unknown")),
            ("Flash", info.get("flash_free_mb", 0) >= 30, "%s MB free" % info.get("flash_free_mb", 0)),
            ("RAM", info.get("mem_free_mb", 0) >= 40, "%s MB free" % info.get("mem_free_mb", 0)),
            ("TMP", info.get("tmp_free_mb", 0) >= 20, "%s MB free" % info.get("tmp_free_mb", 0)),
            ("Internet", bool(info.get("internet")), "Connected" if info.get("internet") else "Not connected"),
        ]
        return {"ready": all(x[1] for x in checks), "checks": checks, "info": info}
