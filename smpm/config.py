# ---------------------------------------------------------------------------------------------
#  Copyright (c) Ian Lucas. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import json
import os
import sys

import smpm.const as const


def read():
    if not os.path.exists(const.CONFIG_PATH):
        return {}
    with open(const.CONFIG_PATH, "r") as f:
        return json.load(f)


def get(key: str):
    try:
        config = read()
        return config[key]
    except:
        return None


def set(key: str, value: str):
    config = read()
    config[key] = value
    with open(const.CONFIG_PATH, "w") as f:
        json.dump(config, f)


def delete(key: str):
    config = read()
    del config[key]
    with open(const.CONFIG_PATH, "w") as f:
        json.dump(config, f)


def cli_set(key: str, value: str):
    if key == None or get(key) == None:
        print("this key does not exist.")
        sys.exit(1)

    if value == None:
        print("value cannot be empty")
        sys.exit(1)

    set(key, value)


def cli_get(key: str):
    if key == None:
        print("key cannot be empty.")
        sys.exit(1)

    print(get(key))
