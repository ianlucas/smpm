# ---------------------------------------------------------------------------------------------
#  Copyright (c) Ian Lucas. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import os
import sys
import urllib.parse

import requests

import smpm.const as const
import smpm.core as core
import smpm.mmsource as mmsource
import smpm.packages as config
import smpm.pathlist as pathlist
import smpm.sourcemod as sourcemod


def handle_download_errors(response: requests.Response):
    if response.status_code == 404:
        print(response.url)
        print("file not found. check if this version is correct.")
        sys.exit(1)
    if response.status_code != 200:
        print("failed to download. please check your connection and try again.")
        sys.exit(1)


def get_package_url(package: dict[str, str]):
    name = package["name"]
    version = package["version"]
    filename = f"{name}-{version}.zip"
    return {
        "download_url": f"https://github.com/ianlucas/smpm-packages/raw/main/{filename}",
        "filename": filename,
    }


def handle_post_download(package: dict[str, str], dest_path: str):
    if pathlist.delete(package["name"]):
        print("removed existing files.")

    core.extract(dest_path, package["name"])
    print("extraction completed.")

    config.set(package["name"], package["version"])
    print(f"installed {package['name']} ({package['version']}).")


def install_mmsource(package: dict[str, str]):
    release = mmsource.get_release_from_package(package)
    package["version"] = release["version"]
    install(release["download_url"], release["filename"], package)


def install_sourcemod(package: dict[str, str]):
    release = sourcemod.get_release_from_package(package)
    package["version"] = release["version"]
    install(release["download_url"], release["filename"], package)


def install_from_file():
    cwd = os.getcwd()
    sourcemod_path = os.path.join(cwd, "sourcemod.txt")
    if not os.path.exists(sourcemod_path):
        print("sourcemod.txt not found.")
        sys.exit(1)
    with open(sourcemod_path, "r") as f:
        packages = f.read().splitlines()
    for package_spec in packages:
        main(package_spec)


def install(download_url, filename, package):
    if config.get(package["name"]) == package["version"]:
        print(f"{package['name']} is already installed ({package['version']}).")
        return
    dest_path = os.path.join(const.DOWNLOADS_PATH, filename)
    if not os.path.exists(dest_path):
        print(f"downloading {filename}...")
        response = requests.get(download_url)
        handle_download_errors(response)
        with open(dest_path, "wb") as f:
            f.write(response.content)
            print("download completed.")
    handle_post_download(package, dest_path)


def install_from_github(repo_url: str):
    result = urllib.parse.urlparse(repo_url)
    if not result.hostname == "github.com":
        print("only github repositories are supported.")
        sys.exit(1)
    parts = result.path.split("/")
    package = {"name": parts[2], "version": "github"}
    filename = f"{package['name']}-github.zip"
    download_url = f"https://github.com{result.path}/archive/refs/heads/master.zip"
    dest_path = os.path.join(const.DOWNLOADS_PATH, filename)
    print(f"downloading {filename}...")
    response = requests.get(download_url, auth=(result.username, result.password))
    handle_download_errors(response)
    with open(dest_path, "wb") as f:
        f.write(response.content)
    handle_post_download(package, dest_path)


def main(package_spec: str):
    if package_spec == None:
        return install_from_file()
    if package_spec.startswith("https://"):
        return install_from_github(package_spec)
    package = core.parse_package_spec(package_spec)
    if len(package["version"]) == 0:
        print("invalid package version")
        sys.exit(1)
    if package["name"] == "sourcemod":
        return install_sourcemod(package)
    if package["name"] == "mmsource":
        return install_mmsource(package)
    release = get_package_url(package)
    install(release["download_url"], release["filename"], package)
