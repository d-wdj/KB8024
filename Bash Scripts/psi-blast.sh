export BLASTDB:=/scratch/blastdb

cd Original # Directory of fasta-format files (as input)
for i in *.fasta
do
  echo "Running $i on PSI-BLAST at $(date +%Y-%m-%d:%H:%M:%S)..."
  time psiblast -query $i -evalue 0.01 -db uniref90.fasta -num_iterations 3  -out ../Output/$i.psiblast -out_ascii_pssm ../PSSM/$i.pssm -num_threads 8
  echo "Finished running PSI-BLAST for $i at $(date +%Y-%m-%d:%H:%M:%S).
  "
done
echo "Job done."
