# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox

from .config import PANEL_NAME, VERSION, EDITION, LEAD_TESTER
from .logger import Logger
from .healthcheck import HealthCheck
from .aiadvisor import AIAdvisor
from .systeminfo import SystemInfo
from .neoboot import NeoBootManager
from .kadodoctor import KadoDoctor
from .backup import BackupCenter
from .restore import RestoreCenter
from .cleaner import SmartCleaner
from .updater import OnlineUpdater
from .plugininstaller import SmartPluginInstaller

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
        Logger.write("Kado Panel v0.7.0 Started")

        self["title"] = Label("%s - %s" % (PANEL_NAME, EDITION))
        self["subtitle"] = Label("Welcome Captain Essam | %s" % VERSION)
        self["footer"] = Label("Lead Tester: %s | Smart Plugin Installer Preview" % LEAD_TESTER)

        self.menu_items = [
            "Health Check",
            "AI Advisor",
            "Smart Plugin Installer",
            "Check Update",
            "Kado Doctor",
            "Backup Preview",
            "Create Backup",
            "Restore Center",
            "Smart Cleaner Preview",
            "System Information",
            "System Report",
            "NeoBoot Manager",
            "Smart Install Preview",
            "View Install Logs",
            "View Logs",
            "About",
            "Exit"
        ]
        self["menu"] = MenuList(self.menu_items)
        self["status"] = Label("Captain Essam Edition\n\nSmart Plugin Installer Preview is available.\n\nSelect an option and press OK.")

        self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.ok, "cancel": self.close}, -1)

    def ok(self):
        current = self["menu"].getCurrent()

        if current == "Health Check":
            result = HealthCheck().run()
            lines = ["Kado Health Check", ""]
            for name, ok, value in result.get("checks", []):
                lines.append("%s : %s (%s)" % ("OK" if ok else "WARN", name, value))
            lines.append("")
            lines.append("System Status: %s" % ("READY" if result.get("ready") else "SAFE MODE"))
            self["status"].setText("\n".join(lines))

        elif current == "AI Advisor":
            health = HealthCheck().run()
            neo = NeoBootManager().detect()
            doctor = KadoDoctor().inspect_latest()
            update = OnlineUpdater().check()
            installer = SmartPluginInstaller().preview()
            self["status"].setText("Kado AI Advisor\n\n%s" % AIAdvisor().advise(health, neo, doctor, update, installer))

        elif current == "Smart Plugin Installer":
            self["status"].setText(SmartPluginInstaller().preview().get("text"))

        elif current == "Check Update":
            result = OnlineUpdater().check()
            lines = ["Kado Online Update", "", "Current: %s" % result.get("current_version"), "Remote : %s" % result.get("remote_version"), "", result.get("message", "Unknown result"), "", "Check only. Auto-install will be added later."]
            self["status"].setText("\n".join(lines))

        elif current == "Kado Doctor":
            self["status"].setText(KadoDoctor().inspect_latest().get("report", "No report."))

        elif current == "Backup Preview":
            self["status"].setText(BackupCenter().preview())

        elif current == "Create Backup":
            self["status"].setText(BackupCenter().create_backup().get("message", "Unknown backup result."))

        elif current == "Restore Center":
            self["status"].setText(RestoreCenter().preview())

        elif current == "Smart Cleaner Preview":
            self["status"].setText(SmartCleaner().preview())

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
            self["status"].setText("Smart Install Preview\n\nNo install will run without:\n1. Health Check\n2. Backup\n3. User confirmation")

        elif current == "View Install Logs":
            self["status"].setText("Kado Install Logs\n\n%s" % Logger.read_install_tail())

        elif current == "View Logs":
            self["status"].setText("Kado Logs\n\n%s" % Logger.read_tail())

        elif current == "About":
            self.session.open(MessageBox, "Kado Panel\n%s\n\n%s\nDeveloped by Captain Essam\nLead Tester: Captain Essam (Kado1957)" % (VERSION, EDITION), MessageBox.TYPE_INFO)

        elif current == "Exit":
            self.close()
