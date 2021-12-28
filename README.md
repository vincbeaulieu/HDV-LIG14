# HDV-LIG14

The HDV-LIG14 dataset encompasses 16384 folding sequences generated using the SPOT-RNA algorithm [1]. The goal of this data is to allow the development of machine learning algorithm to better determine the efficiency in self-cleavage and ligation of a given RNA sequence for the HDV-LIG14.

HDV-LIG14 whole sequences as 14 specifics nucleotide that were modified and are illustrated following the IUPAC nucleotide code [2].

HDV-LIG14 (whole sequence)  
GGACCATTCGAMTCCCATTAGRCTGGKCCGCCTCCTSGCGGCGGGAGTTGSGCKAGGGAGGAASAGYCTTYYCTAGRCTAASGMSCATCGATCCGGTTCGCCGGATCCAAATCGGGCTTCGGTCCGGTTC  

HDV-LIG14 (14 modified nucleotide IUPAC and position)  
M G   R   K   S   K   S   Y   Y   Y   R   S   M   S  
12  21  22  27  37  54  64  67  71  72  77  82  84  85    

The "git" folder hold the code used to launch the algorithm and organize the workspace on GitHub. After each batch of 100 generated, it check for any missing data and regenerate these when missing. Then, it upload to GitHub in batch of 50, to not exceed the 100MB upload limit.

REFERENCES:  
[1] https://github.com/jaswindersingh2/SPOT-RNA  
[2] https://www.bioinformatics.org/sms/iupac.html  
