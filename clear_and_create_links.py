import os.path
from os import path
import time
from common import ROMS_FOLDER
from common import get_drives
from common import clear_symlinks
import traceback



def create_symlinks():
    print("#####################")
    print("# CREATING SYMLINKS #")
    print("#####################")
    print("")
    for drive in get_drives():
        roms_path = drive + ":/" + ROMS_FOLDER
        if path.exists(roms_path):
            print("Existing roms folder found: " + roms_path)
            for console in next(os.walk(roms_path))[1]:
                internal_console_path = "./" + ROMS_FOLDER + console
                external_console_path = roms_path + console
                if path.exists(internal_console_path):
                    print("Internal console [" + internal_console_path + "] already exists, creating a backup")
                    os.rename(internal_console_path, internal_console_path + "_bkp")

                print("Creating symlink " + external_console_path + " -> " + internal_console_path)
                os.symlink(external_console_path, internal_console_path)
                print()
        print()


# print("Internal console [" + internal_console_path + "] is a link, deleting it")
if __name__ == '__main__':
    try:
        clear_symlinks()
        create_symlinks()
    except Exception as e:
        print("An error occurred: " + str(e))
        traceback.print_exc()
    finally:
        time.sleep(10)
