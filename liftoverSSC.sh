#!/bin/bash

# The module for Picard (at least version 2.18 needs to be loaded
module load picard/2.18.0

PATH_TO_FILES='/data/data_repo/castrocp/SSC_pipeline/phase3-1/GenoRefinement/'
OUT_DIR='/data/data_repo/castrocp/SSC_pipeline/phase3-1/GenoRefinement/'
REJECT_DIR='/data/data_repo/castrocp/SSC_pipeline/phase3-1/GenoRefinement/'
REFERENCE='/nfs/boylelabnr_turbo/genomes/hg19/hg19.fa.gz'
CHAIN_FILE='/data/UCSC/LIFTOVER/hg38ToHg19.over.chain.gz'

for file in $PATH_TO_FILES*hiConfDeNovo.vcf.gz

do
	/usr/bin/time -v java -jar $EBROOTPICARD/picard.jar LiftoverVcf I=$file O=$OUT_DIR$(basename $file .vcf.gz).hg19.vcf.gz CHAIN=$CHAIN_FILE REJECT=$REJECT_DIR$(basename $file .vcf.gz).hg19.REJECTED_liftover.vcf.gz R=$REFERENCE |& tee -a $OUT_DIR$(basename $file .vcf.gz).hg19.liftover.log

done
