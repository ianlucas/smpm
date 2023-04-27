import os
import tarfile

HOME_PATH = os.path.expanduser("~")
ROOT_PATH = os.path.join(HOME_PATH, ".sourcemod")
PACKAGES_PATH = os.path.join(ROOT_PATH, "packages.json")
DOWNLOADS_PATH = os.path.join(ROOT_PATH, "downloads")
CSGO_PATH = os.path.join(ROOT_PATH, "csgo")


def setup():
    if not os.path.exists(ROOT_PATH):
        os.mkdir(ROOT_PATH)
    if not os.path.exists(DOWNLOADS_PATH):
        os.mkdir(DOWNLOADS_PATH)
    if not os.path.exists(CSGO_PATH):
        os.mkdir(CSGO_PATH)


def get_pathlist_path(pathlist_name):
    return os.path.join(ROOT_PATH, f"{pathlist_name}_pathlist.txt")


def delete_files_and_empty_dirs(pathlist_name):
    pathlist_path = get_pathlist_path(pathlist_name)
    if not os.path.exists(pathlist_path):
        return False
    with open(pathlist_path, "r") as file:
        paths = file.read().splitlines()
    dirs = []
    for path in paths:
        full_path = os.path.join(CSGO_PATH, path)
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
    return True


def get_file_and_directory_paths(directory):
    paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, directory)
            paths.append(relative_file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            relative_dir_path = os.path.relpath(dir_path, directory)
            paths.append(relative_dir_path)
    return paths


def extract(file_path, pathlist_name):
    dest_path = CSGO_PATH
    with tarfile.open(file_path, "r:gz") as tar:
        tar.extractall(dest_path)
        with open(get_pathlist_path(pathlist_name), "w") as file:
            file.write("\n".join(get_file_and_directory_paths(dest_path)))
