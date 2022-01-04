# MAN PAGE #  
  
## Name:  
batch - SPOT_RNA auto-generator and Git auto-upload in batch sequences  
  
## Synopsis:  
sh batch.sh [batch_size] [stating_index]  
  
## Description:  
SPOT_RNA auto-generator, with batch_size and starting sequence number as inputs. After every generated batch, missing data, if any, are solved, and all the generated data from the SPOT_RNA algorithm is uploaded to GitHub in batch of 50, to not exceed the 100MB upload limit.  
  
## Options:  
Does not take any options.  
  
## Examples:  
$ sh batch.sh 100 0  
> Generating batch/size_100/BATCH_SEQUENCE_0  
> Generating batch/size_100/BATCH_SEQUENCE_100  
> Generating batch/size_100/BATCH_SEQUENCE_200  
> ...  
> Generating batch/size_100/BATCH_SEQUENCE_16300  
  
## Bugs:  
- Ending_index is set to 16383. The program does not take ending index as argument yet. Therefore, the value must be changed in the code itself (batch.sh - line 19) for custom ending index.  
- Please raise an issue to report any other bugs or desired features  
  
## Author:  
Vincent Beaulieu  
  
## Copyright:
(c) 2021-2022 Vincent Beaulieu  
    All rights reserved.  

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  
  
This software utilize the SPOT_RNA software. Additional information and the original source code of jaswindersingh2/SPOT-RNA are available on https://github.com/jaswindersingh2/SPOT-RNA. The jaswindersingh2/SPOT-RNA is licensed under the Mozilla Public License 2.0. More detail on this license at https://github.com/jaswindersingh2/SPOT-RNA/blob/master/LICENSE.  
