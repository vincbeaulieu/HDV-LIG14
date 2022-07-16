
# TODO: This is only test code, will be soon removed


import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# TODO: create setup.py and venv to simplify import
try:
    from Lib14.data_properties import HDV_LIG14
except:
    try:
        print("\033[93m" + "**WARNING** Relative Import Failed - Trying Absolute Import")
        
        import sys

        parentdir = os.path.dirname(currentdir)
        sys.path.insert(0, parentdir)

        from Lib14.data_properties import HDV_LIG14
        print("\033[32m" + "**MESSAGE** Import Process Completed")
    except:
        print("\033[91m" + "**ERROR** Import Process Failed")
finally:
    print("\033[0m")






