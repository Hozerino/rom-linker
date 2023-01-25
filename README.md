# rom-linker
A simple (ugly) script to create symlinks between folders inside a `roms/` folder. Very useful for Emulation Stations.

## How to use them:
1) Add all 3 files on the RetroBat root folder (the script needs to be 1 folder away of the /roms/)
2) Have one (or more) external drives with a folder called "roms" on the ROOT of it
3) Run clear_and_create_links.py to create the links
4) Restart RetroBat or update Game Lists
5) [Optional] Run clear.py to remove the links and make it all like before

## How it works:
Before starting, notice it was tested only by me (by the time I'm writing this) and it was tested on Windows 10, using RetroBat; however as I used the same logic as another script I made for EmuELEC, I'm pretty sure it works the SAME way if you use on other EmulationStation based systems.  
**Basically what it does is:**  
For every external drive, it will look for the roms/ folder, inside of it, if there are any folders, it will create a symbolic link on `C:RetroBat/roms/that_folder` pointing to `external_drive:/roms/that_folder`, that way, when RetroBat accesses `that_folder/`, it will look into the folder inside `external_drive/that_folder`.  
Also, the folder that already existed inside `C:RetroBat/roms` will be renamed to `that_folder_bkp`, which the `clear` part of the script returns to normal (and deletes the symlink).  

## Example:
Say your RetroBat is in `C:/RetroBat`, so your roms folder is `C:/RetroBat/roms`.
You'll put the scripts in `C:/RetroBat/script_here.py`, when you run it, it will look for EVERY drive letter, trying to find the `X:/roms` folder, if it does find it, the script will do as follows:
- Check every console folder inside `X:/roms`, let's say it finds a `X:/roms/n64`
- If there is a console, make a backup of `C:/RetroBat/roms/n64` -> `C:/RetroBat/roms/n64_bkp`
- Create a symbolic link from `C:/RetroBat/roms/n64` to `X:/roms/n64`
So everytime RetroBat looks for roms inside `C:/RetroBat/n64` (which is a symbolic link), it will see the games from the `X:/roms/n64` drive.

## Extra configuration:
On version v2.0.0, a configuration.ini file was added, allowing some tweaks:
- scan_disks - Allows you to force Rom-Linker to scan ONLY certain drives, by default it scans all drives;
- ignore_disks - Skips certain drives, by default it ignores no disks besides the one of the next item;
- ignore_local_disk - Like "ignore_disks", but skips only the drive in which the script is running, default is ON (skip local drive);
- ignore_consoles - Skips certain console folders, by default it skips no console and reads all of them;
- internal_roms_path - Relative path (looking from the script location) of the roms where the links will be created;
- external_roms_path - Path of the roms folder (looking from the root of the external drive);
- auto_close - Defines whether the program will close after executing;
- auto_close_seconds - How many seconds to wait before closing (only works if auto_close is 1).

Don't forget to read the comments inside configuration.ini before making any changes.
