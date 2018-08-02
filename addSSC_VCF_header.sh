#!/bin/bash

HEADER_PATH='/data/data_repo/castrocp/SSC_pipeline/SSC_VCF_header'
TARGET_DIR_PATH='/data/data_repo/castrocp/SSC_pipeline/Siblings/phase1-2_sibs/Denovo/sorted/'
OUT_DIR='/data/data_repo/castrocp/SSC_pipeline/Siblings/phase1-2_sibs/Denovo/added_VCFheader/'

for file in $TARGET_DIR_PATH*

do
	cat $HEADER_PATH $file > $OUT_DIR$(basename $file).vcf   
done
