#!/bin/bash

module load BCFtools/1.3-foss-2017a
module load HTSlib/1.6-foss-2017a #for tabix

PHASE_DIR='/data/data_repo/SSC/SSC_new/phase4'
SAMPLE_FILE='/data/data_repo/castrocp/SSC_pipeline/ID_mapping/ssc_phase4_quads_sample_ids.txt'
OUT_DIR='/data/data_repo/castrocp/SSC_pipeline/phase4/SplitPhase'
BATCH_NUM='fams1-5'

for file in $PHASE_DIR/*.vcf.gz

do
	/usr/bin/time -v bcftools view -Oz -S $SAMPLE_FILE $file -o $OUT_DIR/$(basename $file .vcf.gz).$BATCH_NUM.vcf.gz |& tee $OUT_DIR/$(basename $file .vcf.gz).$BATCH_NUM.log

	tabix -p vcf $OUT_DIR/$(basename $file .vcf.gz).$BATCH_NUM.vcf.gz

done
