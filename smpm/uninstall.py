import sys

import smpm.pathlist as pathlist


def main(package_name: str):
    if pathlist.delete(package_name):
        print(f"{package_name} was uninstalled.")
        sys.exit(1)
    else:
        print("package not found")
        sys.exit(0)
