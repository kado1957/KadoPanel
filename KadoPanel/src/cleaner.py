# -*- coding: utf-8 -*-

import os

class SmartCleaner:
    CLEAN_TARGETS = [
        "/tmp",
        "/home/root/logs",
    ]

    def preview(self):
        lines = ["Smart Cleaner Preview", ""]
        total_files = 0
        for folder in self.CLEAN_TARGETS:
            count = 0
            if os.path.exists(folder):
                try:
                    for name in os.listdir(folder):
                        if name.endswith(".log") or name.endswith(".tmp") or "crash" in name.lower():
                            count += 1
                except Exception:
                    pass
            total_files += count
            lines.append("%s : %s candidate files" % (folder, count))
        lines.append("")
        lines.append("Total candidates: %s" % total_files)
        lines.append("Preview only. No files are deleted in this alpha.")
        return "\n".join(lines)
