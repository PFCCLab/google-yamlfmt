import os
import platform
import sys
import subprocess
import importlib.resources as pkg_resources
from yamlfmt import BIN_NAME

def get_executable_path():
    with pkg_resources.as_file(pkg_resources.files('yamlfmt').joinpath(f"./{BIN_NAME}")) as p:
        executable_path = p

    if platform.system() != "Windows":
        if not os.access(executable_path, os.X_OK):
            current_mode = os.stat(executable_path).st_mode
            os.chmod(executable_path, current_mode | 0o111)

    return executable_path

def main():
    executable_path = get_executable_path()
    result = subprocess.run([executable_path] + sys.argv[1:], check=False)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
