## Setup ##

The Python Virtual Environment (.venv folder) must be placed under the "HDV-LIG14" folder, and *NOT* in the "python" folder. Making the HDV-LIG14 as the working directory to access the SPOT-RNA generated data.

The 'requirements.txt' file holds the libraries requirements to setup the virtual environment. On Mac, in VScode, setup can be initialised by using the commands:  

> python3 -m venv .venv
> source .venv/bin/activate
> python3 -m pip install matplotlib
> python3 -m pip install pandas
> python3 -m pip install tensorflow
> python3 -m pip install scikit-learn

_Ensure the working directory of the Terminal is HDV-LIG14_

More information about setting up the environment on Mac/Windows/Linux can be found here:
https://code.visualstudio.com/docs/python/python-tutorial

If you are still getting errors will running the code, you can do:

> pip freeze

And compare the output with the 'requirements.txt' file and lookup for any discrepancies.

