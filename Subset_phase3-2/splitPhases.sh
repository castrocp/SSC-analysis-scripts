#!/bin/bash

# Use GATK's SelectVariants tool to split the raw VCF chromosome files for a particular phase into multiple VCF files containing a subset of the families included in that phase
module load GATK

PATH_TO_FILES='/data/data_repo/SSC/SSC_new/phase3-2'
OUT_DIR='/data/data_repo/castrocp/SSC_pipeline/phase3-2/SplitPhases/Families_1-75'
REFERENCE='/nfs/boylelabnr_turbo/genomes/hg38/GRCh38_full_analysis_set_plus_decoy_hla.fa'
SAMPLE_FILE='/data/data_repo/castrocp/SSC_pipeline/ID_mapping/ssc_phase3-2_quads_1-75_quads_sample_ids.txt'


# MAKE SURE TO CHANGE THE SUFFIX FOR THE OUTPUT FILE NAME ACCORDING TO WHICH FAMILIES ARE BEING PROCESSED

for file in $PATH_TO_FILES/*.vcf.gz

do
	/usr/bin/time -v java -jar $EBROOTGATK/GenomeAnalysisTK.jar -T SelectVariants -R $REFERENCE -V $file -sf $SAMPLE_FILE -o $OUT_DIR/$(basename $file .vcf.gz).families1-75.vcf.gz |& tee $OUT_DIR/$(basename $file .vcf.gz).families1-75.log
	
done
