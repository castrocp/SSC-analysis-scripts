#!/bin/bash

# The module for Picard (at least version 2.18 needs to be loaded

PATH_TO_FILES='/data/data_repo/castrocp/SSC_pipeline/Siblings/phase1-2_sibs/Denovo/added_VCFheader/'
OUT_DIR='/data/data_repo/castrocp/SSC_pipeline/Siblings/phase1-2_sibs/Denovo/lifted_over_to_hg19/'
REJECT_DIR='/data/data_repo/castrocp/SSC_pipeline/Siblings/phase1-2_sibs/Denovo/lifted_over_to_hg19/'
REFERENCE='/nfs/boylelabnr_turbo/genomes/hg19/hg19.fa.gz'
CHAIN_FILE='/data/UCSC/LIFTOVER/hg38ToHg19.over.chain.gz'

for file in $PATH_TO_FILES*

do
	/usr/bin/time -v java -jar $EBROOTPICARD/picard.jar LiftoverVcf I=$file O=$OUT_DIR$(basename $file .sorted.denovo.vcf).denovo.hg19.vcf CHAIN=$CHAIN_FILE REJECT=$REJECT_DIR$(basename $file .sorted.denovo.vcf).denovo.rejectedLiftover.vcf R=$REFERENCE |& tee -a /data/data_repo/castrocp/SSC_pipeline/Siblings/phase1-2_sibs/Denovo/lifted_over_to_hg19/liftover.log

done
