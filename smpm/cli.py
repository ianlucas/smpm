# ---------------------------------------------------------------------------------------------
#  Copyright (c) Ian Lucas. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import argparse

import smpm.compile as compile
import smpm.config as config
import smpm.core as core
import smpm.install as install
import smpm.uninstall as uninstall


def main():
    core.setup()

    parser = argparse.ArgumentParser(description="smpm")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    install_help = "Name of the package to install"
    install_parser = subparsers.add_parser("install", help="Install a package")
    install_parser.add_argument("package_spec", nargs="?", help=install_help)

    uninstall_help = "Name of the package to uninstall"
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a package")
    uninstall_parser.add_argument("package_name", help=uninstall_help)

    compile_f_help = "Filename to be compiled"
    compile_r_help = "Root of the plugin directory"
    compile_parser = subparsers.add_parser("compile", help="Compile a plugin")
    compile_parser.add_argument("-f", "--file", help=compile_f_help)
    compile_parser.add_argument("-r", "--root", help=compile_r_help)

    get_key_help = "Key of the configuration"
    get_parser = subparsers.add_parser("get", help="Get a configuration value")
    get_parser.add_argument("key", help=get_key_help)

    set_key_help = "Key of the configuration"
    set_value_help = "Value of the configuration"
    set_parser = subparsers.add_parser("set", help="Set a configuration value")
    set_parser.add_argument("key", help=set_key_help)
    set_parser.add_argument("value", help=set_value_help)

    args = parser.parse_args()

    if args.command == "install":
        install.main(args.package_spec)
    if args.command == "uninstall":
        uninstall.main(args.package_name)
    if args.command == "compile":
        compile.main(args.file, args.root)
    if args.command == "set":
        config.cli_set(args.key, args.value)
    if args.command == "get":
        config.cli_get(args.key)


if __name__ == "__main__":
    main()
