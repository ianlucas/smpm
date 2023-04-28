import os

import smpm.const as const


def get_path(pathlist_name):
    return os.path.join(const.ROOT_PATH, f"{pathlist_name}_pathlist.txt")


def delete(pathlist_name):
    pathlist_path = get_path(pathlist_name)
    if not os.path.exists(pathlist_path):
        return False
    with open(pathlist_path, "r") as file:
        paths = file.read().splitlines()
    dirs = []
    for path in paths:
        full_path = os.path.join(const.CSGO_PATH, path)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            dirs.append(full_path)
    for full_path in dirs:
        if os.path.isdir(full_path):
            try:
                os.rmdir(full_path)
            except OSError:
                pass
    os.remove(pathlist_path)
    return True


def write(name, files: list[str]):
    with open(get_path(name), "w") as pathlist:
        pathlist.write("\n".join(files))
