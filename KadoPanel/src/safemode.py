# -*- coding: utf-8 -*-

class SafeMode:
    SAFE_ACTIONS = [
        "Health Check",
        "AI Advisor",
        "System Information",
        "System Report",
        "View Logs",
        "Restart Enigma2"
    ]

    def allowed_actions(self):
        return self.SAFE_ACTIONS
