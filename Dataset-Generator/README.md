# MAN PAGE #  
  
## Name:  
batch.sh, git_add.sh, git_upload.sh, relocate.sh, validate_results.sh, color.sh - SPOT_RNA auto-generator and Git auto-uploader in batch sequences  
  
## Synopsis:  
sh batch.sh [batch_size] [stating_index] [destination_path]
  
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
- Please raise an issue to report any bugs, or to suggest desired features. You can also fork this repo.  
  
## Author:  
Vincent Beaulieu  
  
## Copyright:
(c) 2021-2022 Vincent Beaulieu  
    All rights reserved.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.  

This software utilize the SPOT_RNA software. Additional information and the original source code of jaswindersingh2/SPOT-RNA are available on https://github.com/jaswindersingh2/SPOT-RNA. The jaswindersingh2/SPOT-RNA is licensed under the Mozilla Public License 2.0. More detail on this license at https://github.com/jaswindersingh2/SPOT-RNA/blob/master/LICENSE.  
  
## References:

[1] Padideh Danaee, Mason Rouches, Michelle Wiley, Dezhong Deng, Liang Huang, David Hendrix, bpRNA: large-scale automated annotation and analysis of RNA secondary structure, Nucleic Acids Research, Volume 46, Issue 11, 20 June 2018, Pages 5381–5394, https://doi.org/10.1093/nar/gky285  

[2] H.M. Berman, J. Westbrook, Z. Feng, G. Gilliland, T.N. Bhat, H. Weissig, I.N. Shindyalov, P.E. Bourne. (2000) The Protein Data Bank Nucleic Acids Research, 28: 235-242.  

[3] VARNA: Interactive drawing and editing of the RNA secondary structure Kévin Darty, Alain Denise and Yann Ponty Bioinformatics, pp. 1974-1975, Vol. 25, no. 15, 2009  

[4] Singh, J., Hanson, J., Paliwal, K., Zhou, Y. RNA secondary structure prediction using an ensemble of two-dimensional deep neural networks and transfer learning. Nat Commun 10, 5407 (2019) https://doi.org/10.1038/s41467-019-13395-9  

