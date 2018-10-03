#!/usr/bin/env python3
import gzip
import glob
from os.path import basename
import os
import time

'''
Will process all the multi-family VCF files in a given directory and split them into individual family VCF files.
A mapping file for the project phase being processed should be provided
'''
# Provide path to the directory containing files to be split, output destination, and ID mapping for the phase being processed
DIR_TO_SPLIT = '/data/data_repo/castrocp/SSC_pipeline/Siblings/phase3-1_sibs/GenoRefinement/'
OUT_DIR = '/data/data_repo/castrocp/SSC_pipeline/Siblings/phase3-1_sibs/FamilyVCFs/'
ID_MAP = '/data/data_repo/castrocp/SSC_pipeline/ID_mapping/ssc_phase3-1_quads_id_mapping.txt'


def main():
    # Create dictionaries to match up individual family members with their corresponding sample ID and family ID
    # The family IDs are stored in a list to reference later for creating the file names for each family
    # These only have to be populated once for each phase/mapping file being processed, so they shouldn't be inside a loop
    FamilyMemberDict = {}
    FamilyIdDict = {}
    famIDlist = []

    with open(ID_MAP,"rt") as f:
        for line in f:
            (member,sscID) = line.split()
            famID = member.split(".")[0]

            # Each family ID will be read 4 times (once for each quad family member), so only add it to the list once
            if famID not in famIDlist:
                famIDlist.append(famID)

            # The difference between these is "famID" doesn't have the extension attached. 
            # "member" indicates each family ID along with the member type extension (.fa,.mo,etc.)
            FamilyMemberDict[member] = sscID
            FamilyIdDict[sscID] = famID

    # Split each of the files in the given directory into individual family files
    # Here, I'm splitting the files that have been lifted over to hg19
    for filename in sorted(glob.glob(DIR_TO_SPLIT + '*.hg19.vcf.gz')):
        print("Processing " + basename(filename))
        # The columns for each of the files from the same phase are probably the same, but the Columns list is repopulated for each file here just to be safe
        Columns = []
        
        # Specify to open the gzipped VCF for reading as text ('rt'). Otherwise it will default to binary reading.
        with gzip.open(filename,'rt') as multiFamVCF:
            for line in multiFamVCF:
                
                # This is the header line containing the SSC IDs
                if line.startswith("#CHROM"):
                    Columns=line.strip().split("\t")
                    
                    # Create a dictionary to match up the contents of each column (which, for the header line, is the SSC IDs) with their corresponding column number
                    # Since the columns are stored in a list, the contents of the first column are references as column index 0
                    ColumnDict = {}
                    ColumnIndex = 0
                    
                    for content in Columns:
                        ColumnDict[content] = ColumnIndex
                        ColumnIndex += 1
                    
                    # Create dictionary to link family ID with member extension(.fa,.mo, etc.) to the column index that member's SSC ID is in
                    FamMemColumn={}
                    for member, sscID in FamilyMemberDict.items():
                        FamMemColumn[member] = ColumnDict[sscID]#the column that member id is found in

                    # Once I've used the header to create the necessary dictionaries, stop reading the rest of the file
                    break 
                    # At this point, the loop exits and stops reading lines from multiFamVCF
            
        # Need to re-open and start reading the lines of the file again since the previous loop was broken out of.
        # If I start the "for line" statement without re-opening thf multiFamVCF, it'll start reading from after the
        # "#CHROM" line where the break stopped the line reading 
        
        # Create a file dictionary to access each split family VCF
        file_dict = {}
        family_files =[]
        for famID in famIDlist:
            # This creates/opens a file for each family, and leaves it open for writing (appending) to
            file_object = open(OUT_DIR + '%s' % famID + "." + (os.path.splitext (basename (filename) ) [0]),"a")
            file_dict[famID] = file_object
            
        with gzip.open(filename,'rt') as multiFamVCF:
            for line in multiFamVCF:
                s = time.time()
                line = line.strip("\n").split("\t")
                # Only check the "#CHROM" header line, and all the non-header lines (header lines start with ##)
                if not line[0].startswith("##"):
                    # idx refers to the index number of the line, and val is the content of the corresponding column
                    for idx, val in enumerate(line):
                        #if the SSC id that column index points to ends in .fa, write the first 9 columns, plus that column to the familyID file that SSCID belongs to  
                        for member, col in FamMemColumn.items():
                            if col == idx:
                                if member.endswith(".fa"):
                                    family = member.split(".")[0]
                                    # write to the family file the SSC member ID belongs to
                                    (file_dict[family]).write(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + line[4] + "\t" + line[5] + "\t" + line[6] + "\t" + line[7] + "\t" + line[8] + "\t" + line[idx] + "\t")

         
                    for idx, val in enumerate(line):
                        for member, col in FamMemColumn.items():
                            if col == idx:
                                if member.endswith(".mo"):
                                    family = member.split(".")[0]
                                    (file_dict[family]).write(line[idx] + "\t")

                    for idx, val in enumerate(line):
                        for member, col in FamMemColumn.items():
                            if col == idx:
                                if member.endswith(".s1"):
                                    family = member.split(".")[0]
                                    (file_dict[family]).write(line[idx] + "\t")

                    for idx, val in enumerate(line):
                        for member, col in FamMemColumn.items():
                            if col == idx:
                                if member.endswith(".p1"):
                                    family = member.split(".")[0]
                                    (file_dict[family]).write(line[idx] + "\n")
                


if __name__ == '__main__':
    main()
