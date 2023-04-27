import argparse
import sourcemod.install as install
import sourcemod.core as core
import sourcemod.compile as compile


def main():
    core.setup()

    parser = argparse.ArgumentParser(description="sourcemod")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    install_parser = subparsers.add_parser("install", help="Install a package")
    install_parser.add_argument("package_spec", help="Name of the package to install")

    compile_parser = subparsers.add_parser("compile", help="Compile a plugin")
    compile_parser.add_argument("-f", "--file", help="Filename to be compiled")

    args = parser.parse_args()

    if args.command == "install":
        install.main(args.package_spec)
    elif args.command == "compile":
        compile.main(args.file)


if __name__ == "__main__":
    main()
