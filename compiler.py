import os
import shutil
import sys
from distutils.core import setup
from glob import glob

from Cython.Build import cythonize
from Cython.Distutils import build_ext

PROJECT_DIR = os.path.abspath(".")  # Set the project directory
PROJECT_NAME = os.path.basename(PROJECT_DIR)
DST_DIR = os.path.abspath(os.path.join(".", "lib", PROJECT_NAME))  # Set the destination directory
# Add files you don't want to compile.
EXCLUDE = [
    os.path.abspath(__file__),  # self
    os.path.abspath("main.py")
]

USE_NUMPY = False  # Set whether to use numpy
USE_CDIVISION = False


class Compiler(object):
    def __init__(self):
        self.dirs = [PROJECT_DIR] + glob(os.path.join(PROJECT_DIR, "**/"))
        print()

    @staticmethod
    def get_py_code(subdir):
        files = [os.path.join(subdir, f) for f in os.listdir(subdir)]
        files = [f for f in files if f.endswith(".py") or f.endswith(".pyx")]
        return [os.path.abspath(f) for f in files if f not in EXCLUDE]

    @staticmethod
    def get_c_code(subdir):
        files = [os.path.join(subdir, f) for f in os.listdir(subdir)]
        files = [f for f in files if f.endswith(".c")]
        return [os.path.abspath(f) for f in files if f not in EXCLUDE]

    @staticmethod
    def _compile(subdir: str):
        py_files = Compiler.get_py_code(subdir)
        if not py_files:
            return
        include_dirs = []
        if USE_NUMPY:
            try:
                import numpy
                include_dirs += [numpy.get_include()]
            except Exception:
                print("Numpy is required, but not found. Please install it")
                raise
        os.chdir(subdir)
        ext_modules = cythonize(
            py_files,
            compiler_directives={"language_level": "3", "cdivision": USE_CDIVISION}
        )
        setup(
            cmdclass={"build_ext": build_ext},
            ext_modules=ext_modules,
            include_dirs=include_dirs,
        )

    def compile(self):
        sys.argv = [sys.argv[0], "build_ext", "--inplace"]
        for subdir in self.dirs:
            self._compile(subdir)

    @staticmethod
    def package():
        if os.path.exists(DST_DIR):
            raise FileExistsError(f"Destination directory already exists: {DST_DIR}")
        file_type = "*.so" if sys.platform == "linux" else "*.pyd"
        files = glob(os.path.join(PROJECT_DIR, '**', file_type), recursive=True)
        for file in files:
            rel_path = os.path.relpath(file, start=PROJECT_DIR)
            dst_file = os.path.join(DST_DIR, rel_path)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.move(file, dst_file)
        print(f"All library files have been packaged to {DST_DIR}.")

    def cleanup(self):
        paths = []
        for subdir in self.dirs:
            for file in self.get_c_code(subdir) + ["build"]:
                path = os.path.join(subdir, file)
                if os.path.exists(path):
                    print("Found :", path)
                    paths.append(path)
        if input(f"Remove above temp files? (y/n): ").lower() != "y":
            return
        for path in paths:
            if os.path.exists(path):
                print(f"Removing {path}")
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)


def main():
    compiler = Compiler()
    compiler.compile()
    compiler.package()
    compiler.cleanup()


if __name__ == "__main__":
    main()
