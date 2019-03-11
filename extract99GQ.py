#!/usr/bin/env python3

# Apply this script to a VCF file containing genotypes for quad families, retaining only the lines in which the proband's GQ score is 99
# Since I have already filtered on GQ > 20, the other 3 family members will still have GQ >20

import sys
import glob
import os

DIR = '/data/data_repo/castrocp/SSC_pipeline/Siblings/phase4_sibs/Candidate_DeNovo/VCF/' # Fams376-450/VCF/'
OUT_DIR = '/data/data_repo/castrocp/SSC_pipeline/Siblings/phase4_sibs/Candidate_DeNovo/VCF/' #Fams376-450/VCF/'

def main():

    # child_of_interest = sys.argv[1] # User should input either "sibling" or "proband", depending on which child should be filtered to GQ=99
    
    for file in sorted(glob.glob(DIR + '*.homRefSib')):

        with open(file, 'r') as infile:
            with open(OUT_DIR + "/" + os.path.basename(file) + ".GQ99", "w") as outfile:
                for line in infile:
                    if line.startswith("#"): # header line
                        outfile.write(line)
                    else:
                        cols = line.split()
                        geno_format = cols[8].split(":") # cols[8] is the 9th column, which is the FORMAT column, showing the genotype information fields
                    
                        if geno_format[4] == "GQ": # check which field the GQ score is in.  It will either be the 5th or 6th field, varying per line
                            gq = cols[11].split(":")[4] # The GQ score for the current line
                        else:
                            gq = cols[11].split(":")[5]  # Look at cols[12] for probands, and cols[11] for sibling
                    
                        if gq == "99":
                            outfile.write(line)

if __name__=='__main__':
        main()
