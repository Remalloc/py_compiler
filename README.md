# py_compiler
Compile Python source code into a dynamic library.

### Installation
Place the compiler.py file in your project root path.

```shell script
# Install gcc and python3
pip install Cython
```

## Getting Started
Configure the "INCLUDE" and "EXCLUDE" variables in `compiler.py`.

**Do not compile the entry file, you must add it to "EXCLUDE"**
```shell script 

# The default compiling directory is the base directory of "compiler.py".
python compiler.py
# -d: Specify the compiling directory.
python compiler.py -d /test_project
```

## Deployment
* Only supports Linux systems.
* Requires Python version v3.6 or higher.
