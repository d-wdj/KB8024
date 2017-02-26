# KB8024/8025 [VT17] - Stockholms Universitet
MSc Molecular Techniques in Life Science <br>
2016/2018 <br>
Dimitri Wirjowerdojo<br>

# Predictor Status
ACHIEVEMENTS:
* 02.25 - Enabled multi-threading[8], so each protein takes only up to 5 minutes. Split list of proteins [total=399] into two and ran them separately, runtime should be around several hours, not days.
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
* 02.25 - Improve psi-blast bash script by, skipping .fasta that has been processed. Also add echo $time to see that it is indeed still running.
* ~~02.25 - Split the psi-blast dataset into 6 parts and run them in parallel, run time should be about 2 days.~~
* ~~02.23 - Run psi-blast remotely and retrieve the PSSM.~~
* ~~02.22 - Find out if zeroes are the best way to not ignore the first and last residues. ~~<br>
* ~~02.21 - Create prompt for window size.~~ <br>

PROBLEMS/ISSUES:
* ~~02.25 - Each protein takes about 36 minutes to be run with 3 iterations on psi-blast, meaning it will take about 9 days for 399 proteins.~~
* ~~02.25 - psi-blast can be run but gives an error about composition based matrix.~~
* ~~02.21 - How to not ignore the first and the last residue~~.
