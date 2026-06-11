import os.path
from os import path

from configuration import Configuration

from clear import clear_symlinks
from common import print_cute_message
from common import BACKUP_SUFFIX

import sys
import time

def create_symlinks(config: Configuration):
    print_cute_message("# [CREATE] STARTING #")

    total = 0
    if config.dry_run:
        print("\tDRY_RUN is enabled. No links, backups, or files will be changed.")

    for drive in config.final_scanned_disks:
        print(f"\tCHECK {drive}:")
        roms_path = f"{drive}:{config.external_roms_path}"
        if path.exists(roms_path):
            print(f"\t\tFOUND [{roms_path}]")
            for console in next(os.walk(roms_path))[1]:
                if console in config.ignore_consoles:
                    print(f"\t\tIGNORING [{console}] as configured")
                    continue
                internal_console_path = f"{config.internal_roms_path + console}"
                external_console_path = roms_path + console
                if path.exists(internal_console_path) and not path.islink(internal_console_path):
                    print(f"\t\tBACKUP [{internal_console_path}] -> [{internal_console_path + BACKUP_SUFFIX}]")
                    if not config.dry_run:
                        os.rename(internal_console_path, internal_console_path + BACKUP_SUFFIX)
                elif path.islink(internal_console_path):
                    print(
                        f"\t\tSKIPPING_LINK [{internal_console_path}] POINTS_TO [{os.readlink(internal_console_path)}]")
                    continue
                action = "WOULD_CREATE_LINK" if config.dry_run else "CREATING_LINK"
                print(f"\t\t{action} [{external_console_path}] -> [{internal_console_path}]")
                total += 1
                if not config.dry_run:
                    os.symlink(external_console_path, internal_console_path)
        else:
            print(f"\t\tSKIPPING {drive}:")

    action = "WOULD BE CREATED" if config.dry_run else "CREATED"
    final_message = f"# [CREATE] FINISHED - [{str(total)}] SYMLINKS {action} #"
    print_cute_message(final_message)


if __name__ == '__main__':
    config = Configuration()
    try:
        clear_symlinks(config)
        print()
        create_symlinks(config)
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

