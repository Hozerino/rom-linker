import os.path
from os import path
import time
from common import ROMS_FOLDER
from common import get_drives
from clear import clear_symlinks
from common import print_cute_message
import traceback


def create_symlinks():
    print_cute_message("# [CREATE] STARTING #")

    total = 0
    for drive in get_drives():
        print(f"    Starting check on {drive}: drive")
        roms_path = f"{drive}:/{ROMS_FOLDER}"
        if path.exists(roms_path):
            print(f"        Existing roms folder found [{roms_path}]")
            for console in next(os.walk(roms_path))[1]:
                internal_console_path = f"./{ROMS_FOLDER + console}"
                external_console_path = roms_path + console
                if path.exists(internal_console_path) and not path.islink(internal_console_path):
                    print(f"        Internal console [{internal_console_path}] already exists, creating [{internal_console_path}_bkp]")
                    os.rename(internal_console_path, internal_console_path + "_bkp")
                elif path.islink(internal_console_path):
                    print(f"        Skipping already created symlink at [{internal_console_path}] -> [{os.readlink(internal_console_path)}]")
                    continue

                print(f"        Creating symlink [{external_console_path}] -> [{internal_console_path}]")
                total += 1
                os.symlink(external_console_path, internal_console_path)

    final_message = f"# [CREATE] FINISHED - [{str(total)}] SYMLINKS CREATED #"
    print_cute_message(final_message)


if __name__ == '__main__':
    try:
        clear_symlinks()
        print()
        create_symlinks()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
    finally:
        time.sleep(10)
