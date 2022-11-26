import os
import traceback
from os import path

from configuration import Configuration
from common import BACKUP_SUFFIX
from common import print_cute_message
from common import remove_suffix


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
    try:
        clear_symlinks()
    except Exception as e:
        print()
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
    finally:
        input("Press [ENTER] to continue...")
