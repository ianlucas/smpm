import os
import tarfile
import zipfile

import smpm.const as const
import smpm.pathlist as pathlist


def get_platform():
    return "linux" if os.name == "posix" else "windows"


def extract(file_path: str, pathlist_name: str):
    dest_path = const.CSGO_PATH
    if file_path.endswith(".gz.tar"):
        with tarfile.open(file_path, "r:gz") as tar:
            files = tar.getmembers()
            tar.extractall(dest_path)
            pathlist.write(pathlist_name, [member.name for member in files])
    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r:gz") as zip:
            files = zip.namelist()
            zip.extractall(dest_path)
            pathlist.write(pathlist_name, files)


def setup():
    if not os.path.exists(const.ROOT_PATH):
        os.mkdir(const.ROOT_PATH)
    if not os.path.exists(const.DOWNLOADS_PATH):
        os.mkdir(const.DOWNLOADS_PATH)
    if not os.path.exists(const.CSGO_PATH):
        os.mkdir(const.CSGO_PATH)
