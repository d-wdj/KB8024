# Make a directory with a specified name  as the home folder for the project
echo -n "Please specify the folder name: "
read foldername
echo "Creating a folder for project '$foldername'..."
mkdir $foldername
cd $foldername
mkdir Datasets
mkdir Literature
mkdir Results
mkdir ./scripts
mkdir ./bash
mkdir ./input
mkdir ./output
mkdir ./logs
touch readme.txt
echo "Project name: '$foldername'
Property of Dimitri Wirjowerdojo
dawirjowerdojo@gmail.com
Stockholms Universitet - KB8024
Folder created on $(date +%Y-%m-%d)" > readme.txt
echo "Project folder '$foldername' has been created."
