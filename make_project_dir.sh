# Make a directory with a specified name  as the home folder for the project
echo -n "Please specify the folder name: "
read foldername
echo "Creating a folder for project '$foldername'..."
mkdir $foldername
cd $foldername
mkdir Datasets
mkdir Results
mkdir scripts
mkdir bash
mkdir input
mkdir output
mkdir logs
touch readme.txt
echo -n "Please specify contact email: "
read email
echo "Project name: '$foldername'
Property of Dimitri Wirjowerdojo
$email
Stockholms Universitet - KB8024
MSc Molecular Techniques in Life Science
KTH, KI, SU & SciLifeLab - 2016/18
Folder created on $(date)" > readme.txt
echo "Project folder '$foldername' has been created."
