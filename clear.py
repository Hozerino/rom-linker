import os
from os import path

from configuration import Configuration
from common import BACKUP_SUFFIX
from common import print_cute_message
from common import remove_suffix

import sys
import time

def clear_symlinks(config: Configuration):
    print_cute_message("# [CLEAR] STARTING #")
    total = 0
    for console in os.listdir(config.internal_roms_path):
        if path.islink(config.internal_roms_path + console):
            print(f"\tDELETING_LINK [{config.internal_roms_path}{console}] POINTS_TO [{os.readlink(config.internal_roms_path+console)}]")
            os.unlink(config.internal_roms_path + console)
            total += 1

        if console.endswith(BACKUP_SUFFIX):
            original = remove_suffix(console, BACKUP_SUFFIX)
            print(f"\tRESTORING_BACKUP [{config.internal_roms_path + console}] -> [{config.internal_roms_path + original}]")
            os.rename(config.internal_roms_path + console, config.internal_roms_path + original)

    final_message = f"# [CLEAR] FINISHED - [{str(total)}] SYMLINKS DELETED #"
    print_cute_message(final_message)


if __name__ == '__main__':
    config = Configuration()
    try:
        clear_symlinks(config)
    except Exception as e:
        print()
        print(f"An error occurred: {str(e)}")
    finally:
        if config.auto_close == 1:
            for remaining in range(config.auto_close_time, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write(f"Exiting in {remaining} seconds.")
                sys.stdout.flush()
                time.sleep(1)
        else:
            input("Press [ENTER] to continue...")
        exit(0)