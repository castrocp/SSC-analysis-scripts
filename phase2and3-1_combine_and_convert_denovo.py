#!/usr/bin/env python3

"""
Run this script after VCF files have been split by chromosome and families from the SSC phases.
All chromosome files will be combined by family, creating one VCF file per file.  Each family file will then
be filtered down to variants containing a "hiConfDeNovo" tag corrseponding to that family ID.  The remaining 
variants will be filtered to ensure that the sibling is homozygous reference (since the hiConfDeNovo tag ignores this).
Finally, the list of remaining variants will be converted to BED format

This script is meant to be run only on the phase2and3-1 phase. The naming convention of the files and paths will be
different for other phases.

The script requires the user to input the families to be processed as a range.  These are the groups that phase2and3-1 were split into.

You also need to type "proband" or "sibling" after the range depending on which child is being processed. The child that is
selected will be the one checked for de novo variants

Run as: 
python combine_and_convert_denovo.py 151-225 proband

That will process the probands from families from the batch of 151-225 (of the 1132 total families in phase2and3-1)
"""

import sys
import subprocess
import glob
import os.path
from os.path import basename

try:
    fams = sys.argv[1]
except: 
    print("Enter the range of families to be processed after the script name")

try:
    child = sys.argv[2]
except:
    print("Enter 'proband' or 'sibling' after the family range")

FAM_IDS = '/data/data_repo/castrocp/SSC_pipeline/ID_mapping/phase2and3-1/ssc_phase2and3-1_quads_' + fams + '_family_ids.txt'
PHASE_DIR = '/data/data_repo/castrocp/SSC_pipeline/phase2and3-1'
ID_MAP = '/data/data_repo/castrocp/SSC_pipeline/ID_mapping/phase2and3-1/ssc_phase2and3-1_quads_' + fams + '_id_mapping.txt'

# The directory containing the VCFs that have been split by families and chromosomes
# The "Fams#" directory should be created when the VCFs are split
SPLIT_DIR = PHASE_DIR + '/FamilyVCFs/Fams' + fams

# Output directory for the files combined by family
subprocess.run(['mkdir', SPLIT_DIR + '/combined_chroms'])
COMBINED_DIR = SPLIT_DIR + '/combined_chroms'

# Directory for candidate de novo files for appropriate family batch
subprocess.run(['mkdir', PHASE_DIR + '/Candidate_DeNovo/Fams' + fams])
CAND_DENOVO_OUT_DIR = PHASE_DIR + '/Candidate_DeNovo/Fams' + fams

# Output directory for files with hiConfDeNovo tags corresponding to the appropriate family
subprocess.run(['mkdir', CAND_DENOVO_OUT_DIR + '/VCF'])
HICONF_TAG_OUT_DIR = CAND_DENOVO_OUT_DIR + '/VCF'

# Output directory for candidate variant files converted to BED format
subprocess.run(['mkdir', CAND_DENOVO_OUT_DIR + '/BED'])
OUT_BED = CAND_DENOVO_OUT_DIR + '/BED'


def main():
    
    # Combine all chromosome files belonging to the same family; since each file has a header just keep one at the beginning and remove all the extras
    # Remove unlocalized contigs
    # Filter out low GQ and low DP, tagged with "low"
    # Sort the file by chromosome and delete the intermediate files
    bash_cmd = "for f in `cat {0}`; do cat {1}/${{f}}.* | sed -e '1!{{/^#/d;}}' | grep -v -e 'gl0' -e 'low' > {2}/${{f}}.combined_chroms.removed_extra_headers.vcf; (head -n 1 {2}/${{f}}.combined_chroms.removed_extra_headers.vcf && tail -n +2 {2}/${{f}}.combined_chroms.removed_extra_headers.vcf | sort -k1,1 -V -s) > {2}/${{f}}.combined_chroms.vcf; rm {2}/${{f}}.combined_chroms.removed_extra_headers.vcf; done".format(FAM_IDS, SPLIT_DIR, COMBINED_DIR)

    subprocess.run(bash_cmd, shell=True, check=True)

    
    #### Keep only the variants within a family file that have a "hiConfDeNovo" tag referencing that family's proband.

    # Use the ID mapping file to create a dictionary, matching each family member to its SSC ID
    FamilyMemberDict = {}
    with open(ID_MAP, "r") as f:
        for line in f:
            (member, sscID) = line.split()
            FamilyMemberDict[member] = sscID

    # Process each file in the directory containing VCF files combined by family. It is assumed there is just one "combined_chroms" file per family in the directory
    for file in sorted(glob.glob(COMBINED_DIR + '/*')):
        # splitext splits whatever is in () into two parts, splitting at the final "."
        # basename give just the filename attached to the rest of the path (removes ".vcf")
        # combining them removes the ".vcf" and leave the rest of the filename, which contains another "."
        # I split that to get just the family ID from the file name
        famID = (os.path.splitext(basename(file)) [0]).split(".")[0]

        with open(file) as infile:
            with open(HICONF_TAG_OUT_DIR + "/" + famID + ".deNovo.hg19.vcf","w" ) as out_file:
                for line in infile:
                    if FamilyMemberDict[famID + ".p1"] in line:
                        out_file.write(line)

    #### Filter the variants down to those in which the sibling is heterozygous reference.
    #### In the previous step the sibling's GT is ignored, so some of them may be heterozygous
    #### The following is taken from the original script "find-denovo.py"  
    
    # Assign family members to their respective VCF column index, depending on whether processing probands or siblings
    # In this script "childIdx" will always be the one checked for a heterozygous GT
    
    if child == "proband":
        dadIdx = 0
        momIdx = 1  
        siblingIdx = 2
        childIdx = 3
    elif child == "sibling":
        dadIdx = 0
        momIdx = 1
        siblingIdx = 3
        childIdx = 2

    for file in sorted(glob.glob(HICONF_TAG_OUT_DIR + '/*')):

        with open (file, 'r') as infile: 
                with open (file + ".homRefSib", "w") as variantFile:
                        for line in infile:
                                if line.startswith("#"):   # header and info lines start with "#"
                                        variantFile.write(line)
                                else:
                                        is_denovo_variant = process_line(line, momIdx, dadIdx, childIdx, siblingIdx)
                                        if is_denovo_variant == True:
                                                variantFile.write(line)
    
    #### Convert the candidate de novo variant files to BED format
    #### This script assumes the input file naming format os "FamilyID.blahblahb" with the ID being first and followed by a period
    #### The original stand-alone version of this part is from the "convert2bed.py" script
    for file in sorted(glob.glob(HICONF_TAG_OUT_DIR + '/*.homRefSib')):
        familyID = (os.path.splitext(basename(file)) [0]).split(".")[0]

        with open(file) as infile:
            with open (OUT_BED + "/" + familyID + ".deNovo.hg19.bed" ,"w") as Bed:
                for line in infile:
                    if not line.startswith("#"):
                    # skip the header lines
                        (chrom, pos, id, ref, alt, qual, filt, info, format, Fgt, Mgt, Sgt, Pgt)= line.strip("\n").split()
                        probandGT = Pgt.split(":")[0]
                        # Since these are candidate de novo variants, it is assumed the father, mother, sibling genotypes are all homozygous reference
                        Bed.write(chrom + "\t" + str(int(pos)-1) + "\t" + pos + "\t" + ref + "\t" + alt + "\t" + familyID + "\n")
                        #BED format is zero-based; VCF is 1-based
                        #So, BED start coordinate is one less than VCF start.

def process_line(line, momIdx, dadIdx, childIdx, siblingIdx):
        is_denovo_variant = False

        (chrom, pos, ID, ref, alt, qual, Filter, info, format, samples) = line.strip("\n").split("\t", 9)
        samples = samples.split("\t")

        dadgeno = samples[dadIdx]
        momgeno = samples[momIdx]
        childgeno = samples[childIdx]
        siblinggeno = samples[siblingIdx]

        dadAlleles = extract_genes(dadgeno)
        momAlleles = extract_genes(momgeno)
        childAlleles = extract_genes(childgeno)
        siblingAlleles = extract_genes(siblinggeno)

        if dadAlleles == "0/0" and momAlleles == "0/0" and siblingAlleles == "0/0" and (childAlleles == "1/0" or childAlleles == "0/1"): 
                is_denovo_variant = True
                return(is_denovo_variant)

def extract_genes(unparsed_geno):
        # split the data by ":", to access only the genotype
        # first element of the list is the genotype when format is Genotype:Quality:ReadDepth:etc.
        geno = unparsed_geno.split(":")[0]

        # split the genotypes into individual alleles - split on "/" or "|"
        #alleles = re.split(r"/|\|", geno)

        return geno #alleles

    
if __name__ == '__main__':
        main()

