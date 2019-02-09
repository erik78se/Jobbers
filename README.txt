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
```
