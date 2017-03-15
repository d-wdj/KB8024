# The Predictors:
* HSC_Predictor.py is for Single sequence-based Predictor
* FM_Predictor.py is for PSSM-Frequency Matrix-based Predictor
* SM_Predictor.py is for PSSM-Substitution Matrix-based Predictor

# The Models:
Due to large file size, the models have been uploaded somewhere else. To obtain, one can either:
* $ python *_Model_Generator.py (../Datasets/* must also be downloaded)
* $ bash obtain_model.sh


For reason(s) still unknown, 1/3 proteins of the dataset could not be predicted using HSC_Predictor.py. So far, the only pattern recognised is that their length was around 180-230 residues.
