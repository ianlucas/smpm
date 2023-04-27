import os
import sourcemod.core as core
import json


def read():
    if not os.path.exists(core.PACKAGES_PATH):
        return {}
    with open(core.PACKAGES_PATH, "r") as f:
        return json.load(f)


def get(name: str):
    try:
        packages = read()
        return packages[name]
    except:
        return None


def set(name: str, version: str):
    packages = read()
    packages[name] = version
    with open(core.PACKAGES_PATH, "w") as f:
        json.dump(packages, f)
