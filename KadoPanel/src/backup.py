# -*- coding: utf-8 -*-

import os
import time
import tarfile
from .config import BACKUP_DIR
from .logger import Logger

class BackupCenter:
    BACKUP_ITEMS = ["/etc/enigma2", "/etc/tuxbox", "/etc/CCcam.cfg", "/etc/oscam", "/usr/keys", "/etc/kadopanel"]

    def available_items(self):
        return [item for item in self.BACKUP_ITEMS if os.path.exists(item)]

    def preview(self):
        lines = ["Backup Center Pro", ""]
        for item in self.BACKUP_ITEMS:
            lines.append("%s : %s" % ("FOUND" if os.path.exists(item) else "MISSING", item))
        lines.append("")
        lines.append("Target: %s" % BACKUP_DIR)
        return "\n".join(lines)

    def create_backup(self):
        if not os.path.exists("/media/hdd"):
            return {"ok": False, "message": "Backup failed: /media/hdd is not mounted."}
        try:
            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)
        except Exception as e:
            return {"ok": False, "message": "Cannot create backup directory: %s" % e}
        items = self.available_items()
        if not items:
            return {"ok": False, "message": "No backup items found."}
        target = os.path.join(BACKUP_DIR, "KadoBackup-%s.tar.gz" % time.strftime("%Y%m%d-%H%M%S"))
        try:
            with tarfile.open(target, "w:gz") as tar:
                for item in items:
                    tar.add(item, arcname=item.lstrip("/"))
            Logger.write("Backup created: %s" % target)
            return {"ok": True, "message": "Backup created successfully:\n%s" % target, "path": target}
        except Exception as e:
            Logger.write("Backup failed: %s" % e)
            return {"ok": False, "message": "Backup failed: %s" % e}
