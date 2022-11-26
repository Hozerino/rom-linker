import traceback
import configparser
import pathlib
import json

from common import subtract
from common import print_cute_message
import string
from ctypes import windll

def get_all_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuration(metaclass=Singleton):
    def __init__(self):
        print_cute_message("# LOADING CONFIGURATION (configuration.ini) #")
        try:
            config_file = configparser.ConfigParser()
            config_file.read("configuration.ini")
            # Lists
            scan_disks = json.loads(config_file['SCAN']['scan_disks'])
            ignore_disks = json.loads(config_file['IGNORE']['ignore_disks'])
            self.ignore_consoles = json.loads(config_file['IGNORE']['ignore_consoles'])

            # Booleans
            ignore_local_disk = config_file['IGNORE']['ignore_local_disk'] == 1
            if ignore_local_disk:
                local_drive = pathlib.Path.home().drive
                ignore_disks.append(local_drive.strip(':'))

            # Strings
            self.internal_roms_path = validate_path(config_file['PATH']['internal_roms_path'])
            self.external_roms_path = validate_path(config_file['PATH']['external_roms_path'])

            if scan_disks:
                self.final_scanned_disks = subtract(scan_disks, ignore_disks)
            else:
                self.final_scanned_disks = subtract(get_all_drives(), ignore_disks)
        except Exception as e:
            print()
            print(f"An error occurred while loading configuration.ini, error: {str(e)}")
            input("Exiting... Press [ENTER] to continue...")
            quit()

        if scan_disks:
            print(f'\tscan_disks={scan_disks}')
        if ignore_disks:
            print(f'\tignore_disks={ignore_disks}')
        if self.ignore_consoles:
            print(f'\tignore_consoles={self.ignore_consoles}')
        print(f'\tignore_local_disk={ignore_local_disk}')
        print(f'\tinternal_roms_path={self.internal_roms_path}')
        print(f'\texternal_roms_path={self.external_roms_path}')
        print(f'\t(calculated) final_scanned_disks={self.final_scanned_disks}')

def validate_path(path):
    if not path.endswith('/'):
        raise ValueError(f"Invalid path in configuration file \"{path}\". Path strings must end with /")
    return path