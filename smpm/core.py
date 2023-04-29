# ---------------------------------------------------------------------------------------------
#  Copyright (c) Ian Lucas. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import os
import sys
import tarfile
import zipfile

import smpm.const as const
import smpm.pathlist as pathlist


def get_platform():
    return "linux" if os.name == "posix" else "windows"


def extract(file_path: str, pathlist_name: str):
    dest_path = const.CSGO_PATH
    if file_path.endswith(".tar.gz"):
        with tarfile.open(file_path, "r:gz") as tar:
            files = tar.getmembers()
            tar.extractall(dest_path)
            pathlist.write(pathlist_name, [member.name for member in files])
    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip:
            files = zip.namelist()
            zip.extractall(
                dest_path,
                members=[
                    file_info
                    for file_info in zip.infolist()
                    if not os.path.exists(os.path.join(dest_path, file_info.filename))
                ],
            )
            pathlist.write(pathlist_name, files)


def parse_package_spec(package_spec: str):
    parts = package_spec.split("@")
    if len(parts) > 2:
        print("invalid package spec")
        sys.exit(1)
    return {"name": parts[0], "version": "latest" if len(parts) == 1 else parts[1]}


def setup():
    if not os.path.exists(const.ROOT_PATH):
        os.mkdir(const.ROOT_PATH)
    if not os.path.exists(const.DOWNLOADS_PATH):
        os.mkdir(const.DOWNLOADS_PATH)
    if not os.path.exists(const.CSGO_PATH):
        os.mkdir(const.CSGO_PATH)
