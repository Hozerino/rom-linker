
import string
from ctypes import windll
import os
from os import path

# def is_symlink_windows(path):
#     FILE_ATTRIBUTE_REPARSE_POINT = 0x0400
#     return os.path.isdir(path) and (ctypes.windll.kernel32.GetFileAttributesW(unicode(path)) & FILE_ATTRIBUTE_REPARSE_POINT)

ROMS_FOLDER = "roms/"
BACKUP_SUFFIX = "_bkp"


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

def clear_symlinks():
    print("###########################################")
    print("# CLEARING SYMLINKS AND RESTORING BACKUPS #")
    print("###########################################")
    print("")
    internal_roms_path = "./" + ROMS_FOLDER
    for console in next(os.walk(internal_roms_path))[1]:
        if path.islink(internal_roms_path + console):
            print("Link found, deleting it [" + internal_roms_path + console + "]")
            os.unlink(internal_roms_path + console)

        if console.endswith(BACKUP_SUFFIX):
            original = remove_suffix(console, BACKUP_SUFFIX)
            print("Backup found, restoring it - [" + internal_roms_path+console + "] -> [" + internal_roms_path+original + "]")
            if path.exists(internal_roms_path + original):
                print("Deleting OLD (link) [" + internal_roms_path + original + "]")
                os.remove(internal_roms_path + original)
            os.rename(internal_roms_path + console, internal_roms_path + original)
        print()
