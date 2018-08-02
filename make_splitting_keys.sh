#!/bin/bash


DIR_TO_SPLIT='path to the directory containing the files to split'
SPLIT_KEYS_PATH='path to files containing the SSCids grouped by family in the desired order'
OUT_DIR='where to put the split files'
#find a way to get the family id and create a directoy for it and send the split files diretly to that directory

#This will take the second column, which has the SSC IDs, and then split the file into several files of 4 lines each
awk '{print $2}' ssc_phase1-1_quads_id_mapping.txt | split -l 4

#this will create the array "test" with each element being a line from the "xaa" file.  Then write the file with the lines in a differnt order
# so that they're in the order dad, mom, sibling, proband
mapfile -t test <xaa; for i in 0 1 3 2;do echo ${test[$i]} >> xaa.reordered;done

#This works for manually inputting the IDs in the order you want them written.  But a file can be supplied instead(the one created above

bcftools view -Oz -s SSC00004,SSC00005,SSC00006,SSC00003 REI_10816_B01_GRM_WGS_4_2017-04-14_chr10.recalibrated_variants.CGP_ped.tag_lowGQ_DP.snps_passVQSR.vcf.gz -o testing.11006.vcf.gz

#with the file with the IDs in the correct order:
/usr/bin/time -v bcftools view -Oz -S ../../ID_mapping/xaa.reordered REI_10816_B01_GRM_WGS_4_2017-04-14_chr10.recalibrated_variants.CGP_ped.tag_lowGQ_DP.snps_passVQSR.vcf.gz -o split.11006.vcf.gz


# MAYBE I CAN RUN SEVERAL INSTANCES OFF THIS SCRIPT SIMULTANEOUSLY TO PARRALLELIZE IT, SINCE i CAN JUST HAVE EACH INSTANCE SPLIT BY A DIFFERENT GROUP OF FAMILEIES.  tHE SPLITTING KEYS WOULD HAV TO BE IN DIFFERNT DIRECTORIES FROM EACH OTHER SINCE THE SCRIPT WILL LOOP THROUGH THE DIRECTORY AND FOCUS ON SPEICIFC FAMILIES.  
