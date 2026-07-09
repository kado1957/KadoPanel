# -*- coding: utf-8 -*-

from Plugins.Plugin import PluginDescriptor
from .main import KadoPanelMain

def main(session, **kwargs):
    session.open(KadoPanelMain)

def Plugins(**kwargs):
    return [PluginDescriptor(name="Kado Panel", description="Professional Enigma2 Management Panel", where=PluginDescriptor.WHERE_PLUGINMENU, icon="logo.png", fnc=main)]
