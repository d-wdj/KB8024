# KB8024/8025 [VT17] - Stockholms Universitet
MSc Molecular Techniques in Life Science <br>
2016/2018 <br>
Dimitri Wirjowerdojo<br>

# Notice
* For final assignment, please check folder "Final"
* ~~For the task due on 2017.02.27, please check extractor.py~~

# Predictor Status
ACHIEVEMENTS:
* 03.02 - For regular predictor (without evolutionary information/PSI-BLAST PSSM), most efficient (in terms of computing time and performance) is to use LinearSVC rather than SVC (with linear kernel). 
* 03.02 - Task recently done/are currently undertaken:
  * (v) Add evolutionary information by running psi-blast and extracting the information (use either the subtitution matrix or the frequency matrix); and
  * (vii) Optimisation of SVM performance.
* 02.25 - Enabled multi-threading[8] for psi-blast, so each protein takes only up to 5 minutes. Split list of proteins [total=399] into two and ran them separately, runtime should be around several hours, not days.
* 02.24 - Installed BLAST+ package to be run offline (though psi-blast doesn't take -remote flag!).
* 02.24 - Split big script into extractor (+ cross-validation dataset splitting), SVM, PSSM-parser.
* 02.23 - Managed to do task (ii-iv not necessarily in order):
  * (i) Extract the features from dataset;
  * (ii) Create cross-validated sets;
  * (iii) Train a SVM using single sequence information, using sklearn;
  * (iv) Check different window sizes for the inputs; and
  * (vi) Train a SVM using multiple sequence information.
* 02.22 - Created prompt for window size.

GOALS:
* 03.02 - Complete optimisation by Sunday (2017.03.05) and modify the script such that it can take an input sequence(s).
* 02.27 - Try to optimise everything by trying all possible parameter permutations. ~~Possibly do this on multiple threads to speed up process.~~ [Apparently python does not allow that].
* ~~02.26 - Modify code to split dataset for cross-validation on protein-level, rather than window-level.~~
* ~~02.25 - Improve psi-blast bash script by, skipping .fasta that has been processed. Also add echo $time to see that it is indeed still running.~~
* ~~02.25 - Split the psi-blast dataset into 6 parts and run them in parallel, run time should be about 2 days.~~
* ~~02.23 - Run psi-blast remotely and retrieve the PSSM.~~
* ~~02.22 - Find out if zeroes are the best way to not ignore the first and last residues.~~
* ~~02.21 - Create prompt for window size.~~

PROBLEMS/ISSUES:
* 03.02 - COMPUTING POWER IS NOT ENOUGH TO GET RESULTS FASTER. (Though I suppose this will not be resolved anytime soon).
* ~~03.02 - Python was acting funny: length of a list increases by number of zero-padding added despite the list not being touched at all during iteration to add zeroes.~~
* ~~02.25 - Each protein takes about 36 minutes to be run with 3 iterations on psi-blast, meaning it will take about 9 days for 399 proteins.~~
* ~~02.25 - psi-blast can be run but gives an error about composition based matrix.~~
* ~~02.21 - How to not ignore the first and the last residue~~.
