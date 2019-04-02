#!/usr/bin/env python

# This will run an n-base-pair sliding window through the list of candidate denovo SNVs to determine which of them are within n-bps of each other.

# Run as:  ClusterSNV.py inFileName

import sys
import os

def main():

	winSize = int(raw_input("How many base-pairs in size do you want the bins to be? "))
	inFileName = sys.argv[1]

        with open(inFileName) as proband_variants:
            
            filebase = os.path.splitext(inFileName)[0] 	
            with open (filebase + '.clustered%sbp.bed' % winSize, "w") as outfile:
            
                lines = proband_variants.readlines()
                genomic_coord_list = []
                for line in lines:
                    # Read each line one at a time and return the individual columns as elements of the "columns" list
                    columns = line.split()
                    genomic_coord_list.append((columns[0], columns[1]))
                
                # start with the first chromosome
                current_chrom = genomic_coord_list[0][0]

                # user-defined sliding window size
                bin_size = winSize

                # keep track of the variant being processed
                variant_index = 0

                for coord in genomic_coord_list:
                # Calculate the number of variants within the bin for each iteration of this loop
    
                    # This will only occur on the last line, at which point we should stop the search
                    if variant_index == (len(genomic_coord_list) - 1):
                        variant_count = 1
                        # There will only be one variant in this last bin, then stop everything
                        outfile.write(lines[variant_index].strip('\n') + '\t' + str(variant_count) + '\n')
    
                    else:
    
                        # keep track of the number of variants within this bin
                        variant_count = 0
    
                        # use this to move track the lines when searching for variants within the current bin
                        temp_line_index = variant_index 
        
        
                        # make sure you're still within the same chromosome as the previous iteration
                        if coord[0] == current_chrom:
                            bin_end = int(coord[1]) + bin_size 
           
                        else:
                            # once you move to a new chromosome update the variable
                            current_chrom = coord[0]
                            bin_end = int(coord[1]) + bin_size
        
                        # check to see if the start position of the next variant is within the bin
                        while (int(genomic_coord_list[temp_line_index][1]) <= bin_end) and (genomic_coord_list[temp_line_index][0] == current_chrom):
                            variant_count += 1
                            # if a variant is found to be within the bin size, check the next line
                            temp_line_index += 1
    
                        # Use this to keep track of and go back to the next variant in line
                        variant_index += 1
        
                        # Print the line that's being processed along with the number of variants within the window size distance
                        outfile.write(lines[variant_index-1].strip('\n') + '\t' + str(variant_count) + '\n')

if __name__ == '__main__':
	main() 

 
