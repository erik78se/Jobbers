# Jobbers

## Prepare for build
```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
```

## Local development
source venv/bin/activate
pip --timeout 2 install --editable .
jobber

## Build pip package (wheel)
The buildt whl package ends up in "dist" directory
```bash
python setup.py sdist
python setup.py bdist_wheel
```
Packages (tar.gz)  are built in "dist/"

## Install local package with pip
```bash
pip install dist/Jobber-0.1.dev0-py3-none-any.whl
```

## Build snap
```bash
# (if lxd) export SNAPCRAFT_BUILD_ENVIRONMENT=lxd
# (if kvm) export SNAPCRAFT_BUILD_ENVIRONMENT=host

# Clean up previous build
python3 setup.py clean
rp -rf build/ dist/
snapcraft clean
snapcraft

## Install snap (devmode)
sudo snap install --devmode jobbers_0.1.snap

## application will be available as "jobber.<application>"
