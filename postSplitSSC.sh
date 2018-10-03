#!/bin/bash

# Each time this is run on a different set of files, change the paths to the appropriate directories for:
#	-the file containing a list of the family IDs for the phase being processed
#	-the phase being processed
#	-the input and output directories in the 2 denovo calling scripts and convert2bed.py script
# Also make sure to modify the extract_hiConfDeNovo script to indicate whether looking at probands or siblings
# When the command for find-denovo.py is run, type the family members in the correct order depending on looking at probands or siblings

# Paths refer to locations on Poppy
FAM_IDS='/data/data_repo/castrocp/SSC_pipeline/ID_mapping/ssc_phase3-1_quads_family_ids.txt'

# Phase being processed
PHASE_DIR='/data/data_repo/castrocp/SSC_pipeline/phase3-1'

# Directory containing the VCFs that have been split by families and chromosomes (the FamilyVCFs directory should have been created during the splitting step)
SPLIT_DIR=$PHASE_DIR/FamilyVCFs

# Output directory for files combined by family
mkdir $SPLIT_DIR/combined_chroms 
COMBINED_DIR=$SPLIT_DIR/combined_chroms

# Output directory for files with hiConfDeNovo tags corresponding to appropriate family
# The directories are referenced by the "extract_hiConfDeNovo.py" script
mkdir $PHASE_DIR/Candidate_DeNovo
mkdir $PHASE_DIR/Candidate_DeNovo/VCF
mkdir $PHASE_DIR/Candidate_DeNovo/BED
HICONF_TAG_OUT_DIR=$PHASE_DIR/Candidate_DeNovo/VCF
OUT_BED=$PHASE_DIR/Candidate_DeNovo/BED

# Combine all chromosome files belonging to the same family; since each file has a header just keep one at the beginning and remove all the extras
# Remove unlocalized contigs
# Filter out low GQ and low DP, tagged with "low"
# Sort the file by chromosome and delete the intermediate files
for f in `cat $FAM_IDS`; do cat $SPLIT_DIR/${f}.* | sed -e '1!{/^#/d;}' | grep -v -e "gl0" -e "low" > $COMBINED_DIR/${f}.combined_chroms.removed_extra_headers.vcf; (head -n 1 $COMBINED_DIR/${f}.combined_chroms.removed_extra_headers.vcf && tail -n +2 $COMBINED_DIR/${f}.combined_chroms.removed_extra_headers.vcf | sort -k1,1 -V -s) > $COMBINED_DIR/${f}.combined_chroms.vcf; rm $COMBINED_DIR/${f}.combined_chroms.removed_extra_headers.vcf; done

# Call the script that keeps only the variants within a family file if it has a "hiConfDeNovo" tag referencing that family's proband
# IMPORTANT: THE PYTHON SCRIPT NEEDS TO BE MODIFIED TO LOOK FOR THE CORRECT SUFFIX DEPENDING ON WHETHER WORKING WITH PROBAND OR SIBLING FILES (".p1" or ".s1")
# THE DIRECTORIES ALSO NEED TO BE ASSIGNED IN THE PYTHON SCRIPT
python ~/SSCpipeline/extract_hiConfDeNovo.py

# Run the denovo variant caller script that takes the sibling's genotype into account (the script extracting hiConfDeNovo tags ignores sibling GT)
# THIS NEEDS TO BE MODIFIED DEPENDING ON WHETHER PROCESSING PROBANDS OR SIBLINGS. Whichever column is designated as "proband" will be the one
# checked for a heterozygous GT
# ASSIGN THE CORRECT OUTPUT DIRECTORY IN THIS SCRIPT
for file in $HICONF_TAG_OUT_DIR/*.vcf; do python ~/SSCpipeline/find-denovo.py $file dad mom sibling proband; done

# Convert the ouput files from the previous step into BED format
# As with the other scripts, modify the script to indicate the correct directories
python ~/SSCpipeline/convert2bed.py

# Combine all the bed files from the same phase into one
# Modify the output file name according to the phase being processed
cat $OUT_BED/* | sortBed -i > $OUT_BED/phase3-1.deNovo.hg19.bed 

