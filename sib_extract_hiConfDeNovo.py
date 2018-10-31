#!/usr/bin/env python3

import subprocess
import glob
import os.path
from os.path import basename
import re


DIR = '/data/data_repo/castrocp/SSC_pipeline/Siblings/phase3-2_sibs/FamilyVCFs/Fams151-226/combined_chroms/'
OUT_DIR = '/data/data_repo/castrocp/SSC_pipeline/Siblings/phase3-2_sibs/Candidate_DeNovo/Fams151-226/VCF/'
ID_MAP = '/data/data_repo/castrocp/SSC_pipeline/ID_mapping/ssc_phase3-2_quads_151-226_id_mapping.txt'

def main():

    # Use the ID mapping file to create a dictionary, matching each family member to it's SSC ID
    FamilyMemberDict = {}
    with open(ID_MAP, "r") as f:
        for line in f:
            (member, sscID) = line.split()
            FamilyMemberDict[member] = sscID
    
    # Process each file in the directory. It is assumed there is just one "combined_chroms" file per family in the directory
    for file in sorted(glob.glob(DIR + '*')):
        # splitext splits whatever is in () into two parts, splitting at the final "."
        # basename give just the filename attached to the rest of the path (removes ".vcf")
        # combining them removes the ".vcf" and leave the rest of the filename, which contains another "."
        # I split that to get just the family ID from the file name
        famID = (os.path.splitext(basename(file)) [0]).split(".")[0]
        
        with open(file) as infile:
            with open(OUT_DIR + famID + ".deNovo.hg19.vcf","w" ) as out_file:
                for line in infile:
                    # In the version of this script meant to be run on the probands the suffix it will look for is ".p1" instead.
                    # Rather than change the script each time to account for siblings and probands, I just have one copy for each.
                    if FamilyMemberDict[famID + ".s1"] in line:
                        out_file.write(line)
            


if __name__ == '__main__':
    main()


