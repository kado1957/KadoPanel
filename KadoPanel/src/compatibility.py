# -*- coding: utf-8 -*-

SUPPORTED = {
    "OpenBH": {"status": "primary", "tested": ["5.6.008"]},
    "OpenViX": {"status": "planned"},
    "OpenATV": {"status": "planned"},
    "Egami": {"status": "planned"},
    "OpenPLi": {"status": "planned"},
    "PurE2": {"status": "planned"},
}

def is_supported(image):
    return image in SUPPORTED
