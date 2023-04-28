import os
import sys

import requests

import smpm.const as const
import smpm.core as core
import smpm.packages as packages
import smpm.pathlist as pathlist
import smpm.sourcemod as sourcemod


def install_sourcemod(package: dict[str, str]):
    if package["version"] == "latest":
        release = sourcemod.get_url_from_repository()
    else:
        release = sourcemod.get_url_from_package(package)

    package["version"] = release["version"]
    install(release["download_url"], release["filename"], package)


def install(download_url, filename, package):
    if packages.get(package["name"]) == package["version"]:
        print(f"{package['name']} is already installed ({package['version']}).")
        sys.exit(0)
    dest_path = os.path.join(const.DOWNLOADS_PATH, filename)
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

    if pathlist.delete(package["name"]):
        print("removed existing files.")

    core.extract(dest_path, package["name"])
    print("extraction completed.")

    packages.set(package["name"], package["version"])
    print(f"installed {package['name']} ({package['version']}).")


def main(package_spec: str):
    if package_spec == None:
        print("TODO: try to install from sourcemod.txt")
        sys.exit(0)
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
