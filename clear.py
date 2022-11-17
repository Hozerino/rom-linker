from common import clear_symlinks
import time
import traceback

try:
    clear_symlinks()
except Exception as e:
    print("An error occurred: " + str(e))
    traceback.print_exc()
finally:
    time.sleep(10)