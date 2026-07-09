# -*- coding: utf-8 -*-

import os
from .detector import ImageDetector
from .logger import Logger

class SmartPluginInstaller:
    PLUGINS = [
        {
            "name": "AjPanel",
            "category": "Panel",
            "images": ["OpenBH", "OpenATV", "OpenViX", "Egami"],
            "status": "planned",
            "command": ""
        },
        {
            "name": "ElieSat Panel",
            "category": "Panel",
            "images": ["OpenBH", "OpenATV", "OpenViX"],
            "status": "planned",
            "command": ""
        },
        {
            "name": "Email Panel PRO",
            "category": "Panel",
            "images": ["OpenBH", "OpenATV", "OpenViX"],
            "status": "planned",
            "command": ""
        },
        {
            "name": "ExtraEvent",
            "category": "Plugin",
            "images": ["OpenBH", "OpenATV", "OpenViX"],
            "status": "planned",
            "command": ""
        },
        {
            "name": "OSCam",
            "category": "SoftCam",
            "images": ["OpenBH", "OpenATV", "OpenViX", "Egami"],
            "status": "planned",
            "command": ""
        },
        {
            "name": "NCam",
            "category": "SoftCam",
            "images": ["OpenBH", "OpenATV"],
            "status": "planned",
            "command": ""
        }
    ]

    def current_image(self):
        return ImageDetector().detect_image()

    def compatible_plugins(self):
        image = self.current_image()
        return [p for p in self.PLUGINS if image in p.get("images", [])]

    def preview(self):
        image = self.current_image()
        plugins = self.compatible_plugins()
        lines = ["Smart Plugin Installer", "", "Detected Image: %s" % image, "", "Compatible plugins:"]
        if not plugins:
            lines.append("No compatible plugins found yet.")
        else:
            for p in plugins:
                lines.append("- %s [%s] (%s)" % (p["name"], p["category"], p["status"]))
        lines.append("")
        lines.append("Safe Preview Mode: no installation will run in this alpha.")
        Logger.install("Plugin installer preview for image: %s, count=%s" % (image, len(plugins)))
        return {"image": image, "plugins": plugins, "count": len(plugins), "text": "\n".join(lines)}
