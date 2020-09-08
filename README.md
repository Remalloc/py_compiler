# py_compiler
Compile python source code to dynamic library.

### Installing
Copy compiler.py in your project root path.
```shell script
# install gcc,python3
pip install -r requirements
```

## Getting Started
Configure "INCLUDE" and "EXCLUDE" variables in compiler.py.

**Don't compile the entry file, you must add it in "EXCLUDE"**
```shell script 

# Default compiling dir is "compiler.py" base dir.
python compiler.py
# -d: Appoint compiling dir.
python compiler.py -d /test_project
```

## Deployment
* Only support linux system.
* Python version greater than v3.6.
