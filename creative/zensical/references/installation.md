# Zensical Installation Notes

## Important: Zensical is not on crates.io

As of the time of this writing (June 2026), Zensical is not available on crates.io or PyPI via standard `pip install zensical`. Attempting to install from crates.io will get a package that contains only a compile error message directing users to the proper installation method.

## Official Installation Method

Install directly from GitHub releases using the wheel file:

```bash
# Using pip with direct URL
pip install https://github.com/zensical/zensical/releases/download/v0.0.46/zensical-0.0.46-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Using pipx (recommended for isolated installation)
pipx install https://github.com/zensical/zensical/releases/download/v0.0.46/zensical-0.0.46-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

## Finding the Latest Release

To find the latest release for your platform:

1. Visit: https://github.com/zensical/zensical/releases/
2. Look for assets matching your platform:
   - Linux: `zensical-X.X.X-cp310-abi3-manylinux_2_17_X.manylinux2014_X.whl`
   - macOS: `zensical-X.X.X-cp310-abi3-macosx_10_9_X.whl`
   - Windows: `zensical-X.X.X-cp310-abi3-win_amd64.whl`

## Virtual Environment Recommendation

For isolated installation, use a virtual environment:

```bash
python3 -m venv /path/to/venv
source /path/to/venv/bin/activate
pip install https://github.com/zensical/zensical/releases/download/v0.0.46/zensical-0.0.46-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

## Verification

After installation, verify with:
```bash
zensical --version
# Should output: 0.0.46 (or whatever version you installed)
```

## Troubleshooting

- **"zensical isn't on crates.io yet" error**: This means you accidentally installed from crates.io instead of the GitHub release. Uninstall and install from the GitHub URL directly.
- **Missing dependencies**: Ensure you have Python 3.7+ and pip available.
- **Permission errors**: Use `--user` flag with pip or install in a virtual environment if you encounter permission issues.