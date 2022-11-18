import string
from ctypes import windll

ROMS_FOLDER = "roms/"
BACKUP_SUFFIX = "_bkp"

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        while input_string.endswith(suffix):
            input_string = input_string[:-len(suffix)]
    return input_string

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

def print_cute_message(message):
    print("#"*len(message))
    print(message)
    print("#"*len(message))


