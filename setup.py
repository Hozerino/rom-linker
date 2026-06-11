import sys
import subprocess
from pathlib import Path
from shutil import copy2

try:
    import py2exe
except ModuleNotFoundError:
    py2exe = None

from common import print_cute_message


EXECUTABLES = [
    {"script": "clear.py", "dest_base": "clear"},
    {"script": "create_links.py", "dest_base": "create_links"},
    {"script": "configuration_editor.py", "dest_base": "configuration_editor"},
]


def build_with_py2exe():
    if py2exe is None:
        raise ModuleNotFoundError("py2exe")

    print_cute_message("# Creating ROM-LINKER executables #")
    py2exe.freeze(
        console=EXECUTABLES,
        data_files=[("", ["configuration.ini"])],
        options={
            "py2exe": {
                "bundle_files": 3,
                "compressed": True,
                "dist_dir": "dist",
            }
        },
        zipfile="library.zip",
    )
    print()
    print_cute_message("# Successfully created ROM-LINKER executables #")


def build_with_pyinstaller():
    print()
    print_cute_message("# Creating ROM-LINKER executables with PyInstaller #")

    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)

    for target in EXECUTABLES:
        exe_path = dist_dir / f"{target['dest_base']}.exe"
        if exe_path.exists():
            exe_path.unlink()

        subprocess.run(
            [
                sys.executable,
                "-m",
                "PyInstaller",
                "--onefile",
                "--console",
                "--noconfirm",
                "--clean",
                "--distpath",
                "dist",
                "--workpath",
                "build/pyinstaller",
                "--specpath",
                "build/pyinstaller",
                "--name",
                target["dest_base"],
                target["script"],
            ],
            check=True,
        )

    copy2("configuration.ini", dist_dir / "configuration.ini")
    print()
    print_cute_message("# Successfully created ROM-LINKER executables #")


def build_executables():
    if "WindowsApps" in sys.executable:
        print("Windows Store Python detected. Using PyInstaller because py2exe does not support this Python layout.")
        build_with_pyinstaller()
        return

    try:
        build_with_py2exe()
    except Exception as error:
        print()
        print(f"py2exe build failed: {error}")
        print("Falling back to PyInstaller.")
        build_with_pyinstaller()


if __name__ == "__main__":
    build_executables()
