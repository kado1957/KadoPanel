# -*- coding: utf-8 -*-

import time
from .config import LOG_FILE

class Logger:
    @staticmethod
    def write(message):
        try:
            with open(LOG_FILE, "a") as f:
                f.write("[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), message))
        except Exception:
            pass
