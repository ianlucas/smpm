import sys
import requests
import os
import re
import sourcemod.core as core
import sourcemod.packages as packages


def get_platform():
    return "linux" if os.name == "posix" else "windows"


def get_sourcemod_release_ext():
    return "tar.gz" if os.name == "posix" else "windows"


def get_sourcemod_latest_release_regex():
    if os.name == "posix":
        return r"href='[^']+sourcemod-(([^-]+)-git(\d+))-linux\.tar\.gz'"
    return r"href='[^']+sourcemod-(([^-]+)-git(\d+))-windows\.zip'"


# def get_sourcemod_latest_release_regex():
#     platform = "linux" if os.name == "posix" else "windows"
#     version_regex = r"([^-\s]+)"
#     git_revision_regex = r"git(\d+)"
#     return rf"href='[^']+-{version_regex}-{git_revision_regex}-{platform}\.(tar\.gz|zip)'"


def fetch_latest_sourcemod_version():
    response = requests.get("https://www.sourcemod.net/downloads.php?branch=stable")
    match = re.search(get_sourcemod_latest_release_regex(), response.text)
    if not match:
        print("unable to find latest release of sourcemod")
        sys.exit(1)
    dir_version = ".".join(match.group(2).split(".")[:2])
    return match.group(1), dir_version, f"{dir_version}.{match.group(3)}"


def install_sourcemod(package: dict[str, str]):
    if package["version"] == "latest":
        version, dir_version, pkg_version = fetch_latest_sourcemod_version()
    else:
        pkg_version = package["version"]
        parts = pkg_version.split(".")
        version = ".".join(parts[:2]) + f".0-git{parts[2]}"
        dir_version = ".".join(parts[:2])

    if packages.get("sourcemod") == pkg_version:
        print(f"sourcemod is already installed ({pkg_version}).")
        sys.exit(0)

    filename = f"sourcemod-{version}-{get_platform()}.{get_sourcemod_release_ext()}"
    download_url = f"https://sm.alliedmods.net/smdrop/{dir_version}/{filename}"
    dest_path = os.path.join(core.DOWNLOADS_PATH, filename)

    if not os.path.exists(dest_path):
        print(f"downloading {filename}...")
        response = requests.get(download_url)
        if response.status_code == 404:
            print(download_url)
            print("file not found. check if this version is correct.")
            sys.exit(1)
        if response.status_code != 200:
            print("failed to download. please check your connection and try again.")
            sys.exit(1)
        with open(dest_path, "wb") as f:
            f.write(response.content)
            print("download completed.")

    if core.delete_files_and_empty_dirs("sourcemod"):
        print("removed existing files.")

    core.extract(dest_path, "sourcemod")
    print("extraction completed.")

    packages.set("sourcemod", pkg_version)
    print(f"installed sourcemod ({pkg_version}).")


def main(package_spec: str):
    parts = package_spec.split("@")
    if len(parts) > 2:
        print("invalid package spec")
        sys.exit(1)
    package = {"name": parts[0], "version": "latest" if len(parts) == 1 else parts[1]}
    if len(package["version"]) == 0:
        print("invalid package version")
        sys.exit(1)
    if package["name"] == "sourcemod":
        return install_sourcemod(package)
    print("hello")
