import py2exe
from common import print_cute_message

print_cute_message("# Creating CLEAR executable #")
py2exe.freeze(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console=['clear.py'],
    zipfile = None,
)
print_cute_message("Successfull created CLEAR executable")
print()

print_cute_message("Creating CREATE_LINKS executable")
py2exe.freeze(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console=['create_links.py'],
    zipfile = None,
)
print_cute_message("Successfully created CREATE_LINKS executable")