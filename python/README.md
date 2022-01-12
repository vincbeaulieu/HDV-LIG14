## Setup ##  
  
The Python Virtual Environment (.venv folder) must be placed under the "HDV-LIG14" folder, and *NOT* in the "python" folder. Making the HDV-LIG14 as the working directory to access the SPOT-RNA generated data.  
  
The 'requirements.txt' file holds the libraries requirements to setup the virtual environment. On Mac, in VScode, setup can be initialised by using the following commands (make sure python3 is installed prior):    
  
> python3 -m venv .venv  
> source .venv/bin/activate  
> python3 -m pip install matplotlib  
> python3 -m pip install pandas  
> python3 -m pip install tensorflow  
> python3 -m pip install scikit-learn  
  
_Ensure the working directory of the Terminal is HDV-LIG14_  
  
More information about setting up the environment on Mac/Windows/Linux can be found here:  
https://code.visualstudio.com/docs/python/python-tutorial  
  
If you are still getting errors while running the code, you can do:  
  
> pip freeze  
  
And compare the output with the 'requirements.txt' file and lookup for any discrepancies.  
  
## Author:  
Vincent Beaulieu  
  
## Copyright:
(c) 2021-2022 Vincent Beaulieu  
      All rights reserved.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.  
  
This software utilize data generated using the SPOT_RNA software. Additional information and the original source code of jaswindersingh2/SPOT-RNA are available on https://github.com/jaswindersingh2/SPOT-RNA. The jaswindersingh2/SPOT-RNA is licensed under the Mozilla Public License 2.0. More detail on this license at https://github.com/jaswindersingh2/SPOT-RNA/blob/master/LICENSE.  
