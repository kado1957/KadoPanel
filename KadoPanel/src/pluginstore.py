# -*- coding: utf-8 -*-

from .detector import ImageDetector
from .logger import Logger

class PluginStore:
    ITEMS = [
        {"name": "AjPanel", "category": "Panels", "version": "latest", "images": ["OpenBH", "OpenATV", "OpenViX", "Egami"], "description": "Popular Enigma2 panel for plugins and tools.", "status": "planned"},
        {"name": "ElieSat Panel", "category": "Panels", "version": "latest", "images": ["OpenBH", "OpenATV", "OpenViX"], "description": "Panel for Enigma2 add-ons and extensions.", "status": "planned"},
        {"name": "Email Panel PRO", "category": "Panels", "version": "latest", "images": ["OpenBH", "OpenATV", "OpenViX"], "description": "Professional panel package.", "status": "planned"},
        {"name": "ExtraEvent", "category": "Plugins", "version": "latest", "images": ["OpenBH", "OpenATV", "OpenViX"], "description": "Extra event information and graphics.", "status": "planned"},
        {"name": "OSCam", "category": "Softcams", "version": "latest", "images": ["OpenBH", "OpenATV", "OpenViX", "Egami"], "description": "SoftCam emulator.", "status": "planned"},
        {"name": "NCam", "category": "Softcams", "version": "compatible", "images": ["OpenBH", "OpenATV"], "description": "SoftCam emulator, compatibility must be checked.", "status": "planned"},
        {"name": "M3UIPTV", "category": "IPTV", "version": "latest", "images": ["OpenBH", "OpenATV", "OpenViX"], "description": "M3U IPTV list tool.", "status": "planned"},
        {"name": "Device Manager", "category": "Tools", "version": "image-feed", "images": ["OpenBH", "OpenATV", "OpenViX"], "description": "Storage device management when supported by image feed.", "status": "planned"},
        {"name": "Royal Black Gold Skin", "category": "Skins", "version": "concept", "images": ["OpenBH"], "description": "Kado black/gold skin concept.", "status": "concept"},
    ]

    def current_image(self):
        return ImageDetector().detect_image()

    def categories(self):
        cats = sorted(set(item.get("category", "Other") for item in self.ITEMS))
        return cats

    def compatible_items(self):
        image = self.current_image()
        return [item for item in self.ITEMS if image in item.get("images", [])]

    def search(self, keyword):
        keyword = (keyword or "").lower()
        items = self.compatible_items()
        if not keyword:
            return items
        return [item for item in items if keyword in item.get("name", "").lower() or keyword in item.get("category", "").lower() or keyword in item.get("description", "").lower()]

    def store_summary(self):
        image = self.current_image()
        items = self.compatible_items()
        lines = ["Kado Plugin Store", "", "Detected Image: %s" % image, "Categories: %s" % ", ".join(self.categories()), "", "Compatible Items:"]
        for item in items:
            lines.append("- %s [%s] v%s" % (item["name"], item["category"], item["version"]))
        lines.append("")
        lines.append("Store is preview-only in this alpha.")
        Logger.install("Plugin Store viewed for %s, items=%s" % (image, len(items)))
        return {"image": image, "items": items, "items_count": len(items), "categories_count": len(self.categories()), "text": "\n".join(lines)}

    def item_details(self):
        items = self.compatible_items()
        lines = ["Plugin Details Preview", ""]
        for item in items[:8]:
            lines.append("%s" % item["name"])
            lines.append("Category: %s" % item["category"])
            lines.append("Version : %s" % item["version"])
            lines.append("Status  : %s" % item["status"])
            lines.append("Info    : %s" % item["description"])
            lines.append("")
        return "\n".join(lines)
