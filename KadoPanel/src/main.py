# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox

from .config import PANEL_NAME, VERSION, AUTHOR
from .logger import Logger
from .healthcheck import HealthCheck
from .aiadvisor import AIAdvisor

class KadoPanelMain(Screen):
    skin = """
    <screen name="KadoPanelMain" position="center,center" size="900,600" title="Kado Panel">
        <eLabel position="0,0" size="900,600" backgroundColor="#101010" />
        <widget name="title" position="35,25" size="650,45" font="Regular;34" foregroundColor="#d4af37" backgroundColor="#101010" transparent="1" />
        <widget name="subtitle" position="35,70" size="650,35" font="Regular;22" foregroundColor="#ffffff" backgroundColor="#101010" transparent="1" />
        <widget name="menu" position="35,125" size="430,420" font="Regular;24" itemHeight="42" foregroundColor="#ffffff" backgroundColor="#202020" scrollbarMode="showOnDemand" />
        <widget name="status" position="490,125" size="370,420" font="Regular;21" foregroundColor="#ffffff" backgroundColor="#202020" transparent="0" />
        <widget name="footer" position="35,555" size="820,30" font="Regular;20" foregroundColor="#d4af37" backgroundColor="#101010" transparent="1" />
    </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        Logger.write("Kado Panel Started")

        self["title"] = Label("%s - %s" % (PANEL_NAME, VERSION))
        self["subtitle"] = Label("Developed by %s" % AUTHOR)
        self["footer"] = Label("OpenBH 5.6.008 Primary Test | NeoBoot 9.65 Target")

        self.menu_items = [
            "Health Check", "AI Advisor", "Smart Install", "NeoBoot Manager",
            "Kado Profile", "System Information", "Settings", "About", "Exit"
        ]
        self["menu"] = MenuList(self.menu_items)
        self["status"] = Label("Welcome to Kado Panel\n\nPress OK to select an option.")

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
            result = HealthCheck().run()
            self["status"].setText("Kado AI Advisor\n\n%s" % AIAdvisor().advise(result))
        elif current == "About":
            self.session.open(MessageBox, "Kado Panel\n%s\n\nDeveloped by Captain Essam\nPowered by Kado Team" % VERSION, MessageBox.TYPE_INFO)
        elif current == "Exit":
            self.close()
        else:
            self["status"].setText("%s\n\nThis module will be implemented in the next alpha release." % current)
