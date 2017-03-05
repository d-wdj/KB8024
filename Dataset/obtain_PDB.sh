cd ../../Datasets/PDBCull
while read p; do
  echo "Obtaining the PDB file for $p..."
  wget ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb$p.ent.gz
  echo "Processing $p PDB file..."
  gunzip -k pdb$p.ent.gz
  mkdssp -i pdb$p.ent -o $p.dssp
  mv pdb$p.ent.gz Zip
  mv pdb$p.ent Ent
  mv $p.dssp DSSP
done <PDB_Obtain_lower.txt

echo "

Job finished."
