# KB8024/8025 [VT17] - Stockholms Universitet
MSc Molecular Techniques in Life Science <br>
2016/2018 <br>
Dimitri Wirjowerdojo<br>

### •download everything within this folder•

To run the predictor, you may execute the bash script 'HSCPred.sh'. However, it is still a bit wonky(*).
Otherwise, assuming the model has been generated (python *_Model_Generator.py) or downloaded (bash obtain_model.sh), you can run the predictors (single-sequence-, PSSM-Frequency matrix- or PSSM-Substitution matrix-based : python *_Predictor.py) directly inside the folder bin.

Each predictor python script takes three arguments:
$ python *_Predictor.py arg1 arg2 arg3

Where:
* arg1 : Path to filename and fileformat of the test file. Relative to where /bin/ is
* arg2 : Is the name of the output file, which will be saved into a folder called 'Results', one directory above the folder 'bin'.
* arg3 : either 'Y' or 'N', if 'Y' is input then the prediction will be printed onto the terminal.

This predictor can handle multiple sequences in one fasta-format file as long as every sequence is not separated by any linebreak.


(*) Check readme.md file within /bin
