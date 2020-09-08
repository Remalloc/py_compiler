import logging
import os
import sys
import argparse
from collections import defaultdict
from glob import glob
from os.path import splitext

import Cython.Compiler.Options
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import setup, Extension

BASE_DIR = os.path.abspath("..")
INCLUDE = [  # Add you want to compile files.If it empty will compile all files.
]
print(f"INCLUDE: {INCLUDE}")
EXCLUDE = [  # Add you don't want to compile file.
    os.path.abspath(__file__),  # self
    # os.path.join(BASE_DIR,file)
]
print(f"EXCLUDE: {EXCLUDE}")


def pre_print(lines, prefix="-->"):
    """Add prefix in front of the printed message."""
    if isinstance(lines, list) or isinstance(lines, set):
        for i in lines:
            print(prefix, i)
    else:
        print(prefix, lines)


def set_base_dir(path: str):
    """Verify dir path and set execute dir."""
    if not os.path.exists(path):
        raise ValueError(f"Not find {path}.")
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not dir.")
    global BASE_DIR
    BASE_DIR = os.path.abspath(path)


def clean_temp_files(temp: set):
    """Clean temp files after compiling"""
    if not temp:
        return
    pre_print("Below source code files will be removed:")
    pre_print(temp)
    pre_print("Above source code files will be removed, please confirm it.(y/n)")
    confirm = input()
    if confirm.upper() == "Y":
        for p in temp:
            if os.path.exists(p):
                pre_print("Remove", p)
                os.remove(p)


def start_compile():
    py_path = defaultdict(list)
    temp = set()
    build_dirs = set()
    for root, dirs, files in os.walk(BASE_DIR, False):
        for f in files:
            p = os.path.join(root, f)
            if (f.endswith(".py") or f.endswith(".pyx")) and os.stat(p).st_size != 0:
                if (not INCLUDE or p in INCLUDE) and (p not in EXCLUDE):
                    py_path[root].append(p)
                    name = os.path.splitext(p)[0]
                    temp.add(name + ".pyx")
                    temp.add(name + ".py")
                    temp.add(name + ".c")
    for d, p in py_path.items():
        os.chdir(d)
        pre_print(p)
        easycython(False, False, False, *p)
        build_dirs.add(os.path.join(d, "build"))
    clean_temp_files(temp)
    pre_print("The build dirs need to delete manually.")
    pre_print(build_dirs, "rm -rf")
    pre_print("Compile Finish!")


def main():
    if sys.platform != "linux":
        raise OSError(f"Not support {sys.platform}, only linux.")
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="A dir path which is execute compiler")
    args = parser.parse_args()
    if getattr(args, "d"):
        set_base_dir(args.d)
    start_compile()


# Copy from easycython and modify something.

def easycython(annotation=True, numpy_includes=True, debugmode=False, *filenames):
    if debugmode:
        logging.getLogger().setLevel(logging.INFO)

    # The filename args are allowed to be globs
    # files = [f for g in filenames for f in glob(g)
    #          if splitext(f)[1].lower() in [".pyx", ".py", "pyw"]]
    logging.info("Given filenames = " + "\n".join(filenames))
    logging.info("Current dir contents: \n    " + "\n    ".join(os.listdir("..")))
    # This is a beautiful, beautiful line. This is why I use Python.
    files = [f for g in filenames for f in glob(g)]
    logging.info("Detected files: \n    " + "\n    ".join(files))

    # Collect all the extensions to process
    extensions = []
    for f in files:
        basename, ext = splitext(f)
        extensions.append((basename, f))

    # No pyx files given.
    if len(extensions) == 0:
        logging.error("No valid source filenames were supplied.")
        sys.exit(1)

    # Checking for missing files
    missing = [f for n, f in extensions if not os.path.exists(f)]
    if missing:
        logging.error("These files were missing:")
        for f in missing:
            logging.error("    {}".format(f))
        logging.error("Aborting.")
        sys.exit(2)

    sys.argv = [sys.argv[0], "build_ext", "--inplace"]
    Cython.Compiler.Options.annotate = annotation
    # Create module objects
    ext_modules = []
    for n, f in extensions:
        # The name must be plain, no path
        module_name = os.path.basename(n)
        obj = Extension(module_name, [f],
                        extra_compile_args=["-O2", "-march=native"])
        ext_modules.append(obj)

    # Extra include folders. Mainly for numpy.
    include_dirs = []
    if numpy_includes:
        try:
            import numpy
            include_dirs += [numpy.get_include()]
        except Exception as e:
            logging.exception(e)
            logging.exception("Numpy is required, but not found. Please install it")

    setup(
        cmdclass={"build_ext": build_ext},
        include_dirs=include_dirs,
        ext_modules=cythonize(ext_modules, language_level="3")
    )


if __name__ == "__main__":
    main()
