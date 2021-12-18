import sys
import os
import time
import signal
import psutil
import subprocess
import pkg_resources
from constants import PYTHONVERSION

required = {'AnilistPython', "discord"}
required = {lib.lower() for lib in required}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

print(missing)

if missing:
    for lib in missing:
        subprocess.Popen(f"py -{PYTHONVERSION} -m pip install {lib}", shell = True)




