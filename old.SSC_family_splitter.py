#!/usr/bin/env python3
import gzip
import glob
from os.path import basename


'''
Using a single VCF file containing all families mixed together and ID-mapping file, creates and uses dictionaries to group 
family members together and create a new VCF file for each family. Family member columns 1-4 are written as 
father, mother, sibling, proband, respectively.

Will process an entire directory (of which the path must be provided) of multi-family VCF files, separated by chromosome
'''

def main():

    #Create dictionary to link individual family member ID to it's sample ID #
    #Create dictionary to link family ID without extension to a number counting the families
    FamilyMemberdictionary = {}
    FamilyIDdictionary = {}
    counter = 1 #keep track of number of families
    
    # Change this path to use the appropriate mapping file according to which families are being processed
    with open('/data/data_repo/castrocp/SSC_pipeline/ID_mapping/ssc_phase1-1_quads_id_mapping.txt',"rt") as f:   

        for line in f:
            (key, val) = line.split()
            FamilyMemberdictionary[key] = val #keys are family IDs with extension, values are sample IDs


            familyID = key.split(".")[0]  #removes the extension (.fa, .ma, .p1, .s1)

            if familyID not in FamilyIDdictionary:
                FamilyIDdictionary[familyID] = counter #keys are family IDs without extension
                counter += 1
    
    # This path needs to be changed when running this script on different batches of families
    # The path should point to the directory where all of the multi-family VCF files are, to loop through each family
    for filename in sorted(glob.glob('/data/data_repo/castrocp/SSC_pipeline/phase1-1/GenoRefinement/*.snps_passVQSR.vcf.gz')):
        # This is just to help keep track of which families are being processed
        print("Processing " + basename(filename))
        Columns = []
        
        with gzip.open(filename,"rt") as originalVCF:
            for line in originalVCF:
                line = line.strip("\n")
                if line.startswith("#CHROM"):   # This is the line with the column header names 
                    Columns = line.split("\t")

        #Create dictionary to link column numbers to sample ID #s		
        ColumnDictionary = {} 
        counter = 0  #to keep track of column number
        for i in Columns[9:]:  #will start iterating at 10th column, where first SSC ID is found
            ColumnDictionary[counter] = i #keys are column numbers, values are sample IDs
            counter+=1

        #to go through each family ID returning the column that each member of that family is in
        for ID in sorted(FamilyIDdictionary):
            with open (ID + "." + basename(filename), "w") as famVCF: #create one vcf file for each family

                for member, SSC in sorted(FamilyMemberdictionary.items()): #find the SSC# for the father belonging to a particular family
                    if member.startswith(ID) and member.endswith("fa"):  
                        for column, ssc in ColumnDictionary.items(): #find which column the SSC# comes from
                            if ssc == SSC:  
                                fathercolumn = column

                for member, SSC in sorted(FamilyMemberdictionary.items()): 
                    if member.startswith(ID) and member.endswith("mo"): #find mother column
                        for column, ssc in ColumnDictionary.items(): 
                            if ssc == SSC:  
                                mothercolumn = column
        
                for member, SSC in sorted(FamilyMemberdictionary.items()): 
                    if member.startswith(ID) and member.endswith("s1"):  #find sibling column
                        for column, ssc in ColumnDictionary.items(): 
                            if ssc == SSC:  
                                siblingcolumn = column

                for member, SSC in sorted(FamilyMemberdictionary.items()): 
                    if member.startswith(ID) and member.endswith("p1"): #find proband column
                        for column, ssc in ColumnDictionary.items(): 
                            if ssc == SSC:  
                                probandcolumn = column
                
                with gzip.open(filename,"rt") as originalVCF:
                    for line in originalVCF:
                        line = line.strip("\n").split("\t")
                        if not line[0].startswith("##"): # Will only process the non-header lines
                            # account for first SSC ID column starting at column 10
                            famVCF.write(line[0]+"\t"+line[1]+"\t"+line[2]+"\t"+line[3]+"\t"+line[4]+"\t"+line[5]+"\t"+line[6]+"\t"+line[7]+"\t"+line[8]+"\t"+line[fathercolumn+9]+"\t"+line[mothercolumn+9]+"\t"+line[siblingcolumn+9]+"\t"+line[probandcolumn+9]+"\n")  			
						 

if __name__ == '__main__':
	main()
