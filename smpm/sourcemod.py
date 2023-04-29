# ---------------------------------------------------------------------------------------------
#  Copyright (c) Ian Lucas. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import os
import re
import sys

import requests

import smpm.core as core


def get_release_ext():
    return "tar.gz" if os.name == "posix" else "zip"


def get_release_regex():
    version = r"([^-]+)"  # [2]
    git = r"git(\d+)"  # [3]
    filename_version = rf"({version}-{git})"  # [1]
    platform = core.get_platform()
    ext = get_release_ext()
    return rf"href='[^']+sourcemod-{filename_version}-{platform}\.{ext}'"


def get_release_filename(filename_version):
    platform = core.get_platform()
    ext = get_release_ext()
    return f"sourcemod-{filename_version}-{platform}.{ext}"


def get_release_url(url_version, filename):
    return f"https://sm.alliedmods.net/smdrop/{url_version}/{filename}"


def get_latest_release():
    response = requests.get("https://www.sourcemod.net/downloads.php?branch=stable")
    match = re.search(get_release_regex(), response.text)
    if not match:
        print("unable to find latest release of sourcemod")
        sys.exit(1)

    url_version = ".".join(match.group(2).split(".")[:2])
    filename_version = match.group(1)
    filename = get_release_filename(filename_version)
    version = f"{url_version}.{match.group(3)}"

    return {
        "download_url": get_release_url(url_version, filename),
        "filename": filename,
        "version": version,
    }


def get_release(package: dict[str, str]):
    parts = package["version"].split(".")
    url_version = ".".join(parts[:2])
    filename_version = ".".join(parts[:2]) + f".0-git{parts[2]}"
    filename = get_release_filename(filename_version)

    return {
        "download_url": get_release_url(url_version, filename),
        "filename": filename,
        "version": package["version"],
    }


def get_release_from_package(package: dict[str, str]):
    if package["version"] == "latest":
        return get_latest_release()
    return get_release(package)
