# ---------------------------------------------------------------------------------------------
#  Copyright (c) Ian Lucas. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import json
import os

import smpm.const as const


def read():
    if not os.path.exists(const.PACKAGES_PATH):
        return {}
    with open(const.PACKAGES_PATH, "r") as f:
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
    with open(const.PACKAGES_PATH, "w") as f:
        json.dump(packages, f)


def delete(name: str):
    packages = read()
    del packages[name]
    with open(const.PACKAGES_PATH, "w") as f:
        json.dump(packages, f)
