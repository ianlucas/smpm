# ---------------------------------------------------------------------------------------------
#  Copyright (c) Ian Lucas. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import os
import platform
import sys

import smpm.const as const
import smpm.packages as config
import smpm.process as process


def get_os_architecture():
    architecture = platform.architecture()[0]
    return "64" if "64" in architecture else ""


def get_executable():
    return f"spcomp{get_os_architecture()}" if os.name == "posix" else "spcomp.exe"


def main(filter_file: str, root_path: str):
    cwd = os.getcwd()
    if not root_path == None:
        cwd = os.path.join(cwd, root_path)
    if config.get("sourcemod") == None:
        print("sourcemod is not installed.")
        sys.exit(1)
    scripting_path = os.path.join(const.CSGO_PATH, "addons/sourcemod/scripting")
    include_path = os.path.join(scripting_path, "include")
    compiler_path = os.path.join(scripting_path, get_executable())

    if not os.path.exists(compiler_path):
        print(compiler_path)
        sys.exit(1)

    input_sm_path = os.path.join(cwd, "addons/sourcemod")
    input_plugins_path = os.path.join(input_sm_path, "plugins")
    input_scripting_path = os.path.join(input_sm_path, "scripting")
    input_include_path = os.path.join(input_scripting_path, "include")

    if not os.path.exists(input_scripting_path):
        print(f"please create a 'scripting' folder at {input_sm_path}.")

    if not os.path.exists(input_include_path):
        os.mkdir(input_include_path)

    if not os.path.exists(input_plugins_path):
        os.mkdir(input_plugins_path)

    for filename in os.listdir(input_scripting_path):
        if not filename.endswith(".sp"):
            continue
        if filter_file != None and filter_file != filename:
            continue
        input_path = os.path.join(input_scripting_path, filename)
        output_filename = filename.replace(".sp", ".smx")
        output_path = os.path.join(input_plugins_path, output_filename)
        run = process.exec(
            [
                compiler_path,
                input_path,
                "-o",
                output_path,
                "-i",
                include_path,
                "-i",
                input_include_path,
            ],
        )
        print(f"{filename}:")
        print(run["buffer"])
