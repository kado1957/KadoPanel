# -*- coding: utf-8 -*-

from .pluginstore import PluginStore

class SmartPluginInstaller:
    def preview(self):
        return PluginStore().store_summary()
