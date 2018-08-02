#!/usr/bin/python

from itertools import izip_longest

# Read in the SSC family ID mapping file and generate a pedigree file (.ped) for each family.
# The unaffected sibling is not being included since the GATK tools only work for trios

# function for iterating over a group in chunks of "n" size
def grouper(iterable, n):
        args = [iter(iterable)] * n
	return izip_longest(*args)

with open("/data/data_repo/castrocp/SSC_pipeline/ID_mapping/ssc_pilot_quads_id_mapping.txt","r") as key:

	# create a tuple of 4 related family members
	for line in grouper(key,4):

	        # assign elements of tuple to variables
		dad, mom, proband, sibling = line

                # isolate and extract the family ID
		# in family mapping file, each member is listed as (famID.fa/mo/p1/s1), followed by their individual ID
		fam_id = dad.split(".")[0]
				
		# get each individual family member's ID
		dad_id = dad.split("\t")[1].strip()
		mom_id = mom.split("\t")[1].strip()
		proband_id = proband.split("\t")[1].strip()
                sibling_id = sibling.split("\t")[1].strip()

		# generate a file for each family named (famID).list where "famID" is that family's ID#
		with open("/data/data_repo/castrocp/SSC_pipeline/Pedigree_Files/pilot/%s.ped" % fam_id, "w") as ped:
		        # Updated this to create pedigree files for the unaffected SSC sibling
                        #ped.write(fam_id + "\t" + proband_id + "\t" + dad_id + "\t" + mom_id + "\t" + "0" + "\t" + "2" + "\n")
			ped.write(fam_id + "\t" + proband_id + "\t" + dad_id + "\t" + mom_id + "\t" + "0" + "\t" + "2" + "\n")
                        ped.write(fam_id + "\t" + dad_id + "\t" + "0" + "\t" + "0" + "\t" + "1" + "\t" + "1" + "\n")
			ped.write(fam_id + "\t" + mom_id + "\t" + "0" + "\t" + "0" + "\t" + "2" + "\t" + "1" + "\n")
