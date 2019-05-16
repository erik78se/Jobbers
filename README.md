# Jobbers
Jobbers is a Python package that produces so called application "job-scripts".
Those scripts are then ready to be submitted into SLURM.

User local config is located at: ~/.config/Jobbers/config.yaml

# Install snap from snapcraft.io
You can install the software with snap from snapstore:
```sudo snap install jobbers --devmode --edge```

# Running
The snap packages installs scripts (as described in setup.py):
* femfat-jobber
* abaqus-jobber

You can run them as:
```bash
jobbers.abaqus-jobber <some-output-file>
```

## Build & Development Environment
* Build always on Ubuntu 18.04

```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
```
## Build snap

```bash
sudo snap install snapcraft --classic

# (if lxd) export SNAPCRAFT_BUILD_ENVIRONMENT=lxd
# (if kvm) export SNAPCRAFT_BUILD_ENVIRONMENT=host

# Clean up any previous builds
python3 setup.py clean
rm -rf build/ dist/
snapcraft clean
snapcraft
```

## Local python development tip
You can install a local version with pip which allows you to edit and test without having to build packages to test scripts etc. This is really useful.
```
source venv/bin/activate
pip --timeout 2 install --editable .
```

## Build pip package (wheel)
The buildt whl package ends up in "dist" directory
```bash
python3 setup.py clean
python3 setup.py sdist
python3 setup.py bdist_wheel
```
Packages (tar.gz)  are built in "dist/"

## Install local package with pip
```bash
pip install dist/Jobbers-0.1.dev0-py3-none-any.whl
```
