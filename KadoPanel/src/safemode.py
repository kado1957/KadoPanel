# -*- coding: utf-8 -*-

class SafeMode:
    SAFE_ACTIONS = ["View Logs", "System Information", "Create Backup", "Clean Temporary Files", "Restart Enigma2"]

    def allowed_actions(self):
        return self.SAFE_ACTIONS
