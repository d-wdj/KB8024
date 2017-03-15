#!/bin/bash
echo -e "
#########################################################################
##                                                                     ##
##  \e[36;1;7m--(C)2017 Dimitri Wirjowerdojo - KI/KTH/SU-Stockholm, Sweden.--\e[0m    ##
##             MSc Molecular Techniques in Life Science                ##
##---------------------------------------------------------------------##
##                                                                     ##
##    This is a programme which you can use to predict the secondary   ##
##   structure of an input protein. The model is based on 399 proteins ##
##                  with DSSP 3-class assignments.                     ##
##                                                                     ##
#########################################################################
"
sleep 1
echo "Initialising..."
sleep 3
echo "Checking for models..."

function modelcheck {
  modelcheck="True"
  if [ $modelcheck == "True" ] ; then
    while [ ! -f bin/HSC.pkl ] ; do
      echo "Single-sequence predictor model not found."
      read -p "[1]Download [2]Generate in-house: " yn
      case $yn in
        [1]* )  wget -O bin/HSC.pkl "https://studki-my.sharepoint.com/personal/dimitri_wirjowerdojo_stud_ki_se/_layouts/15/guestaccess.aspx?docid=19b17f73483f84d0eb5f6aeee594f529d&authkey=AdDN3w20mDcqh3qSIKmzyO8" -q --show-progres ;;
        [2]* ) cd bin ; python HSC_Model_Generator.py ; cd .. ;;
        * ) echo "Please input '1' to Download or '2' to generate locally." ;;
      esac
    done

    while [ ! -f bin/FM.pkl ] ; do
      echo "PSSM-Frequency Matrix-based predictor model not found."
      read -p "[1]Download [2]Generate in-house: " yn
      case $yn in
        [1]* ) wget -O bin/FM.pkl "https://studki-my.sharepoint.com/personal/dimitri_wirjowerdojo_stud_ki_se/_layouts/15/guestaccess.aspx?docid=0593b2b0d6b3e4b818d735390cef84ccb&authkey=ATCodfV9L6G0tBmrUCRnSY8" -q --show-progress ;;
        [2]* ) cd bin ; python FM_Model_Generator.py ; cd .. ;;
        * ) echo "Please input '1' to Download or '2' to generate locally." ;;
      esac
    done

    while [ ! -f bin/SM.pkl ] ; do
      echo "PSSM-Substitution Matrix-based predictor model not found."
      read -p "[1]Download [2]Generate in-house: " yn
      case $yn in
        [1]* ) wget -O bin/SM.pkl "https://studki-my.sharepoint.com/personal/dimitri_wirjowerdojo_stud_ki_se/_layouts/15/guestaccess.aspx?docid=05578af110f024b0b906aa699302ecfc5&authkey=AU3RFNSrP1axyfWKFSoCMxc" -q --show-progress ;;
        [2]* ) cd bin ; python SM_Model_Generator.py ; cd .. ;;
        * ) echo "Please input '1' to Download or '2' to generate locally." ;;
      esac
    done

    echo "Models exist.
    "
    modelcheck="False"
  fi
}
modelcheck # THIS IS A FUNCTION TO CHECK FOR EXISTENCE OF MODEL FILES

echo -e "\e[32mInput sequence must be in a two-line fasta-format, without empty line separation between each sequence.\e[0m
"
sleep 1
echo -e "Example:
 ____________________________________
|>protein1                           |
|SEQUENCE1SEQUENCE1SEQUENCE1SEQUENCE1|
|>protein2                           |
|\e[4mSEQUENCE2SEQUENCE2SEQUENCE2SEQUENCE2\e[0m|
"

echo -e "Please specify the directory and the name of your fasta-format file. Note that the path/to/file is \e[91mrelative to where the folder bin is located.\e[0m"
echo "bin directory:" && cd bin && pwd && cd ..

echo ""
read -p "Path/to/file.format: " fasta

echo "
Please specify how you would like the output be named."
read -p "Output Name: " outputname

echo "
"
read -p "Would you like the prediction to be displayed on screen [y/n]? " yesno
case $yesno in
  [Yy]* ) yesno="Y" ;;
  [Nn]* ) yesno="N" ;;
* ) echo "Please input 'Y' or 'N'."
esac

while [ ! exitcheck == "False" ] ; do
  echo "Ready to predict!"
  read -p "
  [1] Single-sequence-based prediction
  [2] PSSM-Frequency matrix-based prediction
  [3] PSSM-Substitution matrix-based prediction
  [A] Run on all predictive methods
  [Q] Exit
  Selection: " predict

  cd bin
  case $predict in
    [1]* ) python HSC_Predictor.py ${fasta} ${outputname} ${yesno} && cd .. ;;
    [2]* ) python FM_Predictor.py ${fasta} ${outputname} ${yesno} && cd .. ;;
    [3]* ) python SM_Predictor.py ${fasta} ${outputname} ${yesno} && cd .. ;;
    [Aa]* ) echo "Running [1], [2] and [3] sequentially..." && python HSC_Predictor.py ${fasta} ${outputname} ${yesno} && python FM_Predictor.py ${fasta} ${outputname} ${yesno} && python SM_Predictor.py ${fasta} ${outputname} ${yesno} && cd .. ;;
    [Qq]* ) exitcheck="False" ; cd .. ; break ;;
    * ) echo "Please input '1', '2', '3' or 'A'."
  esac

done
echo "
"
read -p "Would you like to retain PSI-BLAST output files [y/n]? " psisave
case $psisave in
  [Yy]* ) ;;
  [Nn]* ) cd Temp && rm -r * ;;
  * ) echo "Please input 'Y' or 'N'"
esac
echo -e "

Thank you for using this predictor. I hope you get what you came for.
Have a good day! \e[94m(C) 2017 - Dimitri Wirjowerdojo\e[0m
"
