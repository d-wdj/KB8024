export BLASTDB:=/local_uniref/uniref/uniref90

cd Original # Directory of fasta-format files (as input)
for i in *.fasta
do
  if [ ! -f ../Output/$i.psiblast ] ; then 
  echo "Running $i on PSI-BLAST at $(date +%Y-%m-%d:%H:%M:%S)..."
  time psiblast -query $i -evalue 0.01 -db uniref90.fasta -num_iterations 3  -out ../Output/$i.psiblast -out_ascii_pssm ../PSSM/$i.pssm -num_threads 8
  echo "Finished running PSI-BLAST for $i at $(date +%Y-%m-%d:%H:%M:%S).
  "
  fi
done
echo "Job done."
