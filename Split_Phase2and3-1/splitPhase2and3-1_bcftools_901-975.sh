#!/bin/bash

module load BCFtools/1.3-foss-2017a
module load HTSlib/1.6-foss-2017a #for tabix

PHASE_DIR='/data/data_repo/SSC/SSC_new/phase2and3-1'
SAMPLE_FILE='/data/data_repo/castrocp/SSC_pipeline/ID_mapping/phase2and3-1/ssc_phase2and3-1_quads_901-975_sample_ids.txt'
OUT_DIR='/data/data_repo/castrocp/SSC_pipeline/phase2and3-1/SplitPhase/Fams901-975'
BATCH_NUM='fams901-975'

for file in $PHASE_DIR/*.vcf.gz

do
	/usr/bin/time -v bcftools view -Oz -S $SAMPLE_FILE $file -o $OUT_DIR/$(basename $file .vcf.gz).$BATCH_NUM.vcf.gz |& tee $OUT_DIR/$(basename $file .vcf.gz).$BATCH_NUM.log

	tabix -p vcf $OUT_DIR/$(basename $file .vcf.gz).$BATCH_NUM.vcf.gz

done
