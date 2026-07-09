# -*- coding: utf-8 -*-

import json
try:
    from urllib.request import urlopen
except Exception:
    urlopen = None

from .config import VERSION, REMOTE_VERSION_URL
from .logger import Logger

class OnlineUpdater:
    def _normalize(self, value):
        try:
            return [int(x) for x in value.split()[0].split(".")]
        except Exception:
            return [0, 0, 0]

    def check(self):
        if urlopen is None:
            return {"ok": False, "message": "urllib is not available.", "current_version": VERSION}
        try:
            response = urlopen(REMOTE_VERSION_URL, timeout=8)
            raw = response.read().decode("utf-8", "ignore")
            data = json.loads(raw)
            remote = data.get("version", "Unknown")
            update_available = self._normalize(remote) > self._normalize(VERSION)
            Logger.write("Update check: current=%s remote=%s" % (VERSION, remote))
            return {"ok": True, "current_version": VERSION, "remote_version": remote, "update_available": update_available, "message": "Update available" if update_available else "You are using the latest version", "raw": data}
        except Exception as e:
            Logger.write("Update check failed: %s" % e)
            return {"ok": False, "current_version": VERSION, "remote_version": "Unknown", "update_available": False, "message": "Update check failed: %s" % e}
