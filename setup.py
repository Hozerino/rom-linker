import py2exe

print("Creating CLEAR executable")
py2exe.freeze(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console=['clear.py'],
    zipfile = None,
)
print("Successfully created CLEAR executable")
print()

print("Creating CREATE_LINKS executable")
py2exe.freeze(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console=['create_links.py'],
    zipfile = None,
)
print("Successfully created CREATE_LINKS executable")