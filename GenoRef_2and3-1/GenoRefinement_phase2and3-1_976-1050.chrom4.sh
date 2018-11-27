#!/bin/bash

# Each time this is run on a different set of files, change the paths to the appropriate directories for:
#	-input VCFs (the directory all the VCFs to process are in)
#	-output directory for VCFs and log files
# 	-pedigree file depending on whether processing probands or siblings (only trios are supported.
#		Use the "allPhases" version that includes all families.

# Load GATK module
module load GATK/3.8-0-Java-1.8.0_144
module load picard/2.18.0
module load VCFtools/0.1.14

# Paths refer to locations on Poppy, though I've set directories/files (except for original SSC VCFs) up on foxglove to mirror poppy.
PHASE_DIR='/data/data_repo/castrocp/SSC_pipeline/phase2and3-1/SplitPhase/Fams976-1050/chrom4/'
OUT_DIR='/data/data_repo/castrocp/SSC_pipeline/phase2and3-1/GenoRefinement/Fams976-1050/'
PED='/data/data_repo/castrocp/SSC_pipeline/Pedigree_Files/allPhases_quadsOnly.ped'
REF_FILE='/nfs/boylelabnr_turbo/genomes/hg38/GRCh38_full_analysis_set_plus_decoy_hla.fa'
SUPPORTING='/nfs/boylelab_turbo/data_repo/1000genomes/hg38/1000G.phase3.integrated.sites_only.no_MATCHED_REV.hg38.vcf'
# For liftover (reference needs to be the reference for the build I'm lifting TO)
REFERENCE='/nfs/boylelabnr_turbo/genomes/hg19/hg19.fa.gz'
CHAIN_FILE='/data/UCSC/LIFTOVER/hg38ToHg19.over.chain.gz'

for file in $PHASE_DIR*.gz

do
	# Assign the beginning of the file name to a variable so it can be used when creating the output file name
	base=$(basename $file .vcf.gz)
	
	# CalculateGenotypePosteriors
	# The GATK module needs to be loaded for this to work
	# /usr/bin/time -v will output memory usage and time
	# |$ tee will output progress to StdOut and StdErr, and write log to file
	/usr/bin/time -v java -jar $EBROOTGATK/GenomeAnalysisTK.jar -R $REF_FILE -T CalculateGenotypePosteriors --supporting $SUPPORTING -ped $PED -V:VCF $file -o $OUT_DIR$base.CGP_ped.vcf.gz -pedValidationType SILENT |& tee $OUT_DIR$base.CGP_ped.log
	
	# Tag genotypes with GQ<20 or DP<10
	# Variants aren't removed, only tagged with "low"
	/usr/bin/time -v java -jar $EBROOTGATK/GenomeAnalysisTK.jar -T VariantFiltration -R $REF_FILE -V:VCF $OUT_DIR$base.CGP_ped.vcf.gz -G_filter "GQ < 20.0 || DP < 10.0" -G_filterName low -o $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.vcf.gz |& tee $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.log
	
	# Delete Intermediate file
	rm $OUT_DIR$base.CGP_ped.vcf.gz

	# Tag possible de novos
	# Variants may be tagged with "loConfDenovo" or "hiConfDenovo" along with the sample ID the tag refers to
	/usr/bin/time -v java -jar $EBROOTGATK/GenomeAnalysisTK.jar -T VariantAnnotator -A PossibleDeNovo -R $REF_FILE -ped $PED -V:VCF $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.vcf.gz -o $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.vcf.gz -pedValidationType SILENT |& tee $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.log
	
	# Delete Intermediate file
        rm $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.vcf.gz

	# Filter down to variants tagged as high confidence de novos.  Keep header lines.
	zgrep -E '#|hiConfDeNovo' $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.vcf.gz | gzip > $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.hiConfDeNovo.vcf.gz
	
	# Delete Intermediate file
	rm $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.vcf.gz

	# Filter out variants that aren't bi-allelic SNPS and variants that don't "PASS" VQSR
	vcftools --gzvcf $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.hiConfDeNovo.vcf.gz --remove-indels --remove-filtered-all --max-alleles 2 --recode --recode-INFO-all --stdout | gzip -c > $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.hiConfDeNovo.snps_passVQSR.vcf.gz
	
	# Liftover from hg38 to hg19
	/usr/bin/time -v java -jar $EBROOTPICARD/picard.jar LiftoverVcf I=$OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.hiConfDeNovo.snps_passVQSR.vcf.gz O=$OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.hiConfDeNovo.snps_passVQSR.hg19.vcf.gz CHAIN=$CHAIN_FILE R=$REFERENCE REJECT=$OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.hiConfDeNovo.snps_passVQSR.hg19.REJECTED_liftover.vcf.gz |& tee -a $OUT_DIR$base.CGP_ped.tag_lowGQ_DP.tag_possibleDenovo.hiConfDeNovo.snps_passVQSR.hg19.liftover.log


done	
