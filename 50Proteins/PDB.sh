mkdir Temp && cd Temp
mkdir DSSP && mkdir Ent && mkdir Zip
mkdir Fasta && cd Fasta
mkdir Original && mkdir Proces && mkdir Psiblast && mkdir PSSM
cd ../../

cd bin
python extract_pdbcull.py
bash obtain_PDB.sh
python dssp.py
python HSC_counter.py
cd ../Temp/Fasta
echo "Preparing for PSI-BLAST..."
while read p ; do
  if [ -f Original/$p.fasta ] ; then
    cp -v Original/$p.fasta Process/$p.fasta
  fi
done < ForPSIBLAST.txt

export BLASTDB=/local_uniref/uniref/uniref90

cd Process

for i in *.fasta
do
  if [ ! -f ../Psiblast/*.psiblast ] ; then
    echo "Running PSI-BLAST on $i..."
    time psiblast -query $i -db uniref90.db -num_iterations 3 -evalue 0.01 -out ../Psiblast/$i.psiblast -out_ascii_pssm ../PSSM/$i.pssm -num_threads 8
    echo "PSI-BLAST on $i finished."
  fi
done


echo "50 test proteins acquired. Have a good day!"
