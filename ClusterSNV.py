#!/usr/bin/env python

# This will run a 100-base-pair sliding window through the list of candidate denovo SNVs to determine which of them are within 100bps of each other.

# Run as:  ClusterSNV.py inFileName

import sys
import os

def main():

	winSize = int(raw_input("How many base-pairs in size do you want the bins to be? "))
	inFileName = sys.argv[1]

	with open (inFileName) as infile:
            filebase = os.path.splitext(inFileName)[0] 	
            with open (filebase + '.clustered%sbp' % winSize, "w") as outfile:
			#outfile.write("Chrom" + "\t" + "start" + "\t" + "end" + "\t" + "ref" + "\t" + "alt" + "\t" + "geno" + "\t" + "famID" + "\t" + "regDB" + "\t" + "b_start" + "\t" + "b_end" + "\t" + "b_population" + "\n")
			# Write a header to the ouput file
			
			while True:
				line = infile.readline()
				if not line: break
			# Need to run everything after this line of code for each line of the file
			# Each line of the file represents a variant, and there will be a bin for each variant	
				
				bin_pop = 1
				# To keep track of how many variants are found within each bin
			        
                                cols = line.strip("\n").split()
                             
				#(chrom, start, end, ref, alt, famID, regdb) = line.strip("\n").split()
				# Had to add extra columns to make this work with an updated input file format
				# This is the line format in the candidate denovos file after the RegDB annotation step  
				
				start_bin = int(cols[1])
				# The coordinates in the input file are 0-based. I'm using the start coordinate to mark the start of a variant's bin
					
				end_bin = int(cols[1])
				# If no other variant is added to the bin, the bin starts and ends at the same point. Otherwise, the ending point is updated. 		
				current_line_pointer = infile.tell()
				# This variable saves the location of the pointer so we can go back to this line position
				# The pointer is at the end of the line that was just read and parsed
				
				try:
					next_variant_pos = int(infile.readline().strip("\n").split()[1])
					# This is a shortened version of the parsing I did above.
					# Index "1" points to the "start" coordinate of the variant on the next line
				except:
					outfile.write(line.strip("\n") + "\t" + str(start_bin) + "\t" + str(end_bin) + "\t" + str(bin_pop) + "\n")
					break
					# This will only occur when the last line of the input file is being processed
					# Since there is no next line to read, it will just write the last entry to the outfile and finish				

				while next_variant_pos - start_bin <= winSize and next_variant_pos - start_bin > -1:
				# The condition requiring the difference to be positive prevents problems when switching from one chromosome to the next
				# Otherwise, if the next chrom coordinate is smaller than the previous chrom coordinate, it yields a negative number, which is less than winSize
					bin_pop += 1
					# Keeps track of additional variants that fall within the bin
					end_bin = next_variant_pos
					# Updates the end coordinate of the bin
					try:			
						next_variant_pos = int(infile.readline().strip("\n").split()[1])
					# Keeps moving to the next line of the input file to compare the next variant to the current start_bin coordinate
					except:
						break
						
	
				# Once the next variant no longer falls within the bin, exit the loop, write to the output file
				outfile.write(line.strip("\n") + "\t" + str(start_bin) + "\t" + str(end_bin) + "\t" + str(bin_pop) + "\n")

				infile.seek(current_line_pointer)
				# Set the pointer back to the line the bin started at so that it's ready to loop to the next line in order


if __name__ == '__main__':
	main() 

 
