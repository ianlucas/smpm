import argparse

import smpm.compile as compile
import smpm.core as core
import smpm.install as install


def main():
    core.setup()

    parser = argparse.ArgumentParser(description="smpm")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    install_help = "Name of the package to install"
    install_parser = subparsers.add_parser("install", help="Install a package")
    install_parser.add_argument("package_spec", nargs="?", help=install_help)

    compile_help = "Filename to be compiled"
    compile_parser = subparsers.add_parser("compile", help="Compile a plugin")
    compile_parser.add_argument("-f", "--file", help=compile_help)

    args = parser.parse_args()

    if args.command == "install":
        install.main(args.package_spec)
    elif args.command == "compile":
        compile.main(args.file)


if __name__ == "__main__":
    main()
