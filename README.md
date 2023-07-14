# py_compiler
Compile Python source code into a dynamic library.

### Installation
Place the compiler.py file in your project root path.

```shell script
# Install gcc and python3
pip install Cython
```

## Getting Started
Configure the "EXCLUDE" variables in `compiler.py`.

**Do not compile the entry file, you must add it to "EXCLUDE"**

**All `__init__.py` files will be ignored because Cython 2.9 has some problems under the Win32 platform.**
```shell script 

# The default compiling directory is the base directory of "compiler.py".
python compiler.py
```

## Deployment
* Only supports Linux and Win32 systems.
* Requires Python version v3.6 or higher.
