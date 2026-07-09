# -*- coding: utf-8 -*-

SUPPORTED = {
    "OpenBH": {
        "status": "primary",
        "tested": ["5.6.008"],
        "safe_features": ["healthcheck", "systeminfo", "aiadvisor", "neoboot_detect", "report", "doctor", "backup_pro", "online_update_check"]
    },
    "OpenViX": {"status": "planned", "safe_features": ["healthcheck", "systeminfo"]},
    "OpenATV": {"status": "planned", "safe_features": ["healthcheck", "systeminfo"]},
    "Egami": {"status": "planned", "safe_features": ["healthcheck", "systeminfo"]},
    "OpenPLi": {"status": "planned", "safe_features": ["healthcheck", "systeminfo"]},
    "PurE2": {"status": "planned", "safe_features": ["healthcheck", "systeminfo"]},
}

def is_supported(image):
    return image in SUPPORTED

def status(image):
    return SUPPORTED.get(image, {"status": "unknown"}).get("status", "unknown")
