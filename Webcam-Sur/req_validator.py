import sys
import time
import pkg_resources
import subprocess
from platform import python_version
from constants import PYTHONVERSION, REQUIREDLIB

class ReqValidator:
    def validate_python_version(self):
        try:
            assert python_version().find(PYTHONVERSION) != -1
        except:
            print("Error: Specified Python version incorrect. Please ensure the correct Python version is entered in constants.py.")
            print(f"Executing Python Version: {python_version()}")
            print(f"Specifed Python Version: {PYTHONVERSION}")
            sys.exit(0)

    def validate_libraries(self):
        required = REQUIREDLIB
        required = {lib.lower() for lib in required}
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed

        if missing:
            print(f"Warning: Required Libraries Missing >>> {missing}")
            user_input = input("Initiate automatic library installation? Proceed [y/n]")

            if user_input.lower() == 'n':
                print("Program Terminated...")
                sys.exit(0)
            elif user_input.lower() == 'y':
                print("Installing required libraries...")
                for lib in missing:
                    subprocess.run(f"py -{PYTHONVERSION} -m pip install {lib}", shell=True)
                    print(f"Library >{lib}< has been installed.")
            else:
                print("User input unrecognized. Program terminated...")
                sys.exit(0)

            return True # has missing lib (lib installed)
        return False # no missing lib

    def validate_installation(self):
        required = REQUIREDLIB
        required = {lib.lower() for lib in required}
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed

        if missing:
            print(f"Libraries {missing} failed to be installed. Program Terminated.")
            sys.exit(0)
        else:
            print("Library validation complete. All required Libraries has been sucessfully installed.")





if __name__ == "__main__":
    req_validator = ReqValidator()
    req_validator.validate_python_version()
    installed_lib = req_validator.validate_libraries()
