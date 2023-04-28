# smpm

```bash
pip3 install git+https://github.com/ianlucas/smpm.git
```

## Usage

- `smpm install [package_spec]` - install a package
- `smpm uninstall [package_spec]` - uninstall a package
- `smpm compile [-f <file>]` - compiles plugins from the scripting folder

### Defining dependencies

To create a list of dependencies for your project, create a `sourcemod.txt` file in the root directory of your project. Each dependency should be listed on a separate line, like this:

```
json@5.0.0
ptah@1.1.4
```

> **Note**
> The packages are listed on `sourcemod.txt` file in the root of this repository.
