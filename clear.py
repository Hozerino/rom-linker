from common import print_cute_message
from common import ROMS_FOLDER
from common import BACKUP_SUFFIX
from common import remove_suffix
from os import path
import os
import time
import traceback

def clear_symlinks():
    print_cute_message("# [CLEAR] STARTING #")
    internal_roms_path = f"./{ROMS_FOLDER}"
    total = 0
    for console in os.listdir(internal_roms_path):
        if path.islink(internal_roms_path + console):
            print(f"    DELETING_LINK [{internal_roms_path}{console}]")
            os.unlink(internal_roms_path + console)
            total += 1

        if console.endswith(BACKUP_SUFFIX):
            original = remove_suffix(console, BACKUP_SUFFIX)
            print(f"    RESTORING_BACKUP [{internal_roms_path}{console}] -> [{internal_roms_path}{original}]")
            os.rename(internal_roms_path + console, internal_roms_path + original)

    final_message = f"# [CLEAR] FINISHED - [{str(total)}] SYMLINKS DELETED #"
    print_cute_message(final_message)


if __name__ == '__main__':
    try:
        clear_symlinks()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
    finally:
        time.sleep(10)
