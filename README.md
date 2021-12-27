# HDV-LIG14

The HDV-LIG14 dataset encompasses 16384 folding sequences generated using the SPOT-RNA algorithm. The goal of this data is to allow the development of machine learning algorithm to better determine the efficiency in self-cleavage and ligation of a given RNA sequence for the HDV-LIG14.

The "git" folder hold the code used to launch the algorithm and organize the workspace on GitHub. After each batch of 100 generated, it check for any missing data and regenerate these when missing. Then, it upload to GitHub in batch of 50, to not exceed the 100MB upload limit.
