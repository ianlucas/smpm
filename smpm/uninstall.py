# ---------------------------------------------------------------------------------------------
#  Copyright (c) Ian Lucas. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import sys

import smpm.packages as config
import smpm.pathlist as pathlist


def main(package_name: str):
    if pathlist.delete(package_name):
        print(f"{package_name} was uninstalled.")
        config.delete(package_name)
        sys.exit(1)
    else:
        print("package not found")
        sys.exit(0)
