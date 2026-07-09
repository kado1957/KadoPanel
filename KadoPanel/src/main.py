# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox

from .config import PANEL_NAME, VERSION, AUTHOR, EDITION, LEAD_TESTER
from .logger import Logger
from .healthcheck import HealthCheck
from .aiadvisor import AIAdvisor
from .systeminfo import SystemInfo
from .neoboot import NeoBootManager
from .kadodoctor import KadoDoctor

class KadoPanelMain(Screen):
    skin = """
    <screen name="KadoPanelMain" position="center,center" size="1000,650" title="Kado Panel">
        <eLabel position="0,0" size="1000,650" backgroundColor="#101010" />
        <widget name="title" position="35,25" size="800,45" font="Regular;34" foregroundColor="#d4af37" backgroundColor="#101010" transparent="1" />
        <widget name="subtitle" position="35,70" size="800,35" font="Regular;22" foregroundColor="#ffffff" backgroundColor="#101010" transparent="1" />
        <widget name="menu" position="35,125" size="430,465" font="Regular;24" itemHeight="42" foregroundColor="#ffffff" backgroundColor="#202020" scrollbarMode="showOnDemand" />
        <widget name="status" position="490,125" size="470,465" font="Regular;20" foregroundColor="#ffffff" backgroundColor="#202020" transparent="0" />
        <widget name="footer" position="35,605" size="900,30" font="Regular;20" foregroundColor="#d4af37" backgroundColor="#101010" transparent="1" />
    </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        Logger.write("Kado Panel v0.3.0 Started")

        self["title"] = Label("%s - %s" % (PANEL_NAME, EDITION))
        self["subtitle"] = Label("Welcome Captain Essam | %s" % VERSION)
        self["footer"] = Label("Lead Tester: %s | OpenBH 5.6.008 | NeoBoot 9.65" % LEAD_TESTER)

        self.menu_items = [
            "Health Check",
            "AI Advisor",
            "Kado Doctor",
            "System Information",
            "System Report",
            "NeoBoot Manager",
            "Smart Install Preview",
            "View Logs",
            "About",
            "Exit"
        ]
        self["menu"] = MenuList(self.menu_items)
        self["status"] = Label("Captain Essam Edition\n\nInitializing Kado AI Engine...\n\nSelect an option and press OK.")

        self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.ok, "cancel": self.close}, -1)

    def ok(self):
        current = self["menu"].getCurrent()

        if current == "Health Check":
            result = HealthCheck().run()
            lines = ["Kado Health Check", ""]
            for name, ok, value in result.get("checks", []):
                mark = "OK" if ok else "WARN"
                lines.append("%s : %s (%s)" % (mark, name, value))
            lines.append("")
            lines.append("System Status: %s" % ("READY" if result.get("ready") else "SAFE MODE"))
            self["status"].setText("\n".join(lines))

        elif current == "AI Advisor":
            health = HealthCheck().run()
            neo = NeoBootManager().detect()
            doctor = KadoDoctor().inspect_latest()
            self["status"].setText("Kado AI Advisor\n\n%s" % AIAdvisor().advise(health, neo, doctor))

        elif current == "Kado Doctor":
            result = KadoDoctor().inspect_latest()
            self["status"].setText(result.get("report", "No report."))

        elif current == "System Information":
            info = SystemInfo().get_all()
            keys = ["receiver", "image", "image_version", "python", "machine", "kernel", "flash_free_mb", "mem_free_mb", "tmp_free_mb", "internet"]
            self["status"].setText("System Information\n\n" + "\n".join("%s: %s" % (k, info.get(k)) for k in keys))

        elif current == "System Report":
            path = SystemInfo().create_report()
            self["status"].setText("System report created:\n%s" % (path or "Failed"))

        elif current == "NeoBoot Manager":
            neo = NeoBootManager()
            detect = neo.detect()
            images = neo.list_images()
            lines = ["NeoBoot Manager", "", "Installed: %s" % detect.get("installed"), "Path: %s" % detect.get("path"), ""]
            if images:
                lines.append("Detected Images:")
                for item in images[:10]:
                    lines.append("- %s" % item.get("name"))
            else:
                lines.append("No NeoBoot images detected yet.")
            self["status"].setText("\n".join(lines))

        elif current == "Smart Install Preview":
            self["status"].setText("Smart Install Preview\n\nThis module will start after backup safety layer.\n\nNo install will run without Health Check + user confirmation.")

        elif current == "View Logs":
            self["status"].setText("Kado Logs\n\n%s" % Logger.read_tail())

        elif current == "About":
            self.session.open(MessageBox, "Kado Panel\n%s\n\n%s\nDeveloped by Captain Essam\nLead Tester: Captain Essam (Kado1957)" % (VERSION, EDITION), MessageBox.TYPE_INFO)

        elif current == "Exit":
            self.close()
