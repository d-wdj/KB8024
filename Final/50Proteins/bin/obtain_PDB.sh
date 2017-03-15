
#############################################################################
### RUN THIS SECOND
#############################################################################

cd ../Temp
###############################################################################
### OBTAIN dssp FILES
###############################################################################
echo "Checking for DSSP files..."
while read p ; do
  if [ ! -f Zip/pdb$p.ent.gz ] ; then
  echo "Obtaining the PDB file for $p..."
  wget ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb$p.ent.gz -q --show-progress
  echo "Processing $p PDB file..."
  gunzip -k pdb$p.ent.gz
  mkdssp -i pdb$p.ent -o $p.dssp
  mv pdb$p.ent.gz Zip
  mv pdb$p.ent Ent
  mv $p.dssp DSSP
  fi
done <PDB_Obtain_lower.txt

###############################################################################
### OBTAIN 4DIGIT FASTA FILES
###############################################################################
echo "Checking for protein sequence fasta files..."
while read p; do
  if [ ! -f Fasta/'>'$p.fasta ] ; then
  wget -O '>'$p.fasta http://www.rcsb.org/pdb/files/fasta.txt?structureIdList=$p -q --show-progress
  mv -v '>'$p.fasta Fasta/Original
  fi
done < PDB_Obtain_upper.txt
cat Fasta/Original/*.fasta > master.fasta

echo "Obtain PDB finished."
