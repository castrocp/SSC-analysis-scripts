#!/bin/bash

# The PHASE_DIR needs to be manually edited each time this is run.  All other paths are either fixed or will auto-generate based on PHASE_DIR

INFILE_PATH=${1?Error: input the path to file to be filtered after the script name}
PHASE_DIR="/data/data_repo/castrocp/SSC_pipeline/Siblings/phase3-1_sibs"
mkdir $PHASE_DIR/Candidate_DeNovo/BED/filtered_candidates
OUT_DIR=$PHASE_DIR/Candidate_DeNovo/BED/filtered_candidates
INDEL_FILE="/data/data_repo/castrocp/1000genomes/MillsAnd1000gPhase1_combinedGoldStandard.hg19INDELS.bed"
REPEAT_FILE="/home/castrocp/SimpleRepeats/RepeatMasker_TRF_combined.bed"

# Assign the beginning of the file name to a variable so it can be used when creating the output file name
base=$(basename $INFILE_PATH .bed)


# Remove variants that appear in the same exact position in more than one family
awk -F"\t" '{print $1"_"$2}' OFS="\t"  $INFILE_PATH | uniq -c | awk '$1==1 {print $2}' | sed 's/_/\t/g' > $OUT_DIR/$base.sites_appearing_only_once

grep -Ff $OUT_DIR/$base.sites_appearing_only_once $INFILE_PATH > $OUT_DIR/$base.uniqueLoci.bed


# Remove INDELS
bedtools intersect -a $OUT_DIR/$base.uniqueLoci.bed -b $INDEL_FILE -v > $OUT_DIR/$base.uniqueLoci.indelFilt.bed


# Filter out variants that overlap with simple repeats, satellites, and low complexity regions
bedtools intersect -a $OUT_DIR/$base.uniqueLoci.indelFilt.bed -b $REPEAT_FILE -v > $OUT_DIR/$base.uniqueLoci.indelFilt.rptFilt.bed


