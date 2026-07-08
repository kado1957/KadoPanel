# -*- coding: utf-8 -*-

from Plugins.Plugin import PluginDescriptor

def main(session, **kwargs):
    pass

def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="Kado Panel",
            description="Professional Enigma2 Panel",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon="logo.png",
            fnc=main
        )
    ]
