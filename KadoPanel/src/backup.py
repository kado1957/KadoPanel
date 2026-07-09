# -*- coding: utf-8 -*-

import os
import time
from .config import BACKUP_DIR
from .logger import Logger

class BackupCenter:
    BACKUP_ITEMS = [
        "/etc/enigma2/settings",
        "/etc/enigma2/bouquets.tv",
        "/etc/enigma2/bouquets.radio",
        "/etc/tuxbox/config",
        "/usr/keys"
    ]

    def preview(self):
        lines = ["Backup Preview", ""]
        for item in self.BACKUP_ITEMS:
            lines.append(("%s : %s" % ("FOUND" if os.path.exists(item) else "MISSING", item)))
        lines.append("")
        lines.append("Target: %s" % BACKUP_DIR)
        lines.append("This preview does not modify the system.")
        return "\n".join(lines)

    def create_script_hint(self):
        stamp = time.strftime("%Y%m%d-%H%M%S")
        target = os.path.join(BACKUP_DIR, "KadoBackup-%s.tar.gz" % stamp)
        Logger.write("Backup script hint generated: %s" % target)
        return "Future backup target:\n%s\n\nFull backup action will be enabled after safety confirmation layer." % target
