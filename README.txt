# Jobbers

## Prepare
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
```

## Test
```bash
python echo.py
```

## Build package
The build package ends up in "dist" directory
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

snapcraft clean
snapcraft
