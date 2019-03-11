#!/usr/bin/env python3

import sys
import os

'''
Script will read a file that has been annotated by RegulomeDB and scored, and filter out 
unwanted scores.  Output file will only contain the positions with desired scores.

run program as:
filterRegDBscore.py <name of scored file to filter>
'''

def main():

    inFileName = sys.argv[1]

    WantedScores = ["1a","1b","1c","1d","1e","1f","2a","2b","2c","3a","3b"]

    with open (inFileName, 'r') as infile:  #when you use "with open" you don't have to close the file later
        filebase = os.path.splitext(inFileName)[0]
        with open (filebase + ".filteredRegDBscores.bed", "w") as filteredscores: 
            for line in infile:
                (chrom, start, end, refAllele, altAllele, familyID, regscore)=line.strip("\n").split("\t")
		#,rmskchrom,rmskstart,rmskend,rmskstrand,rmskName,rmskclass,rmskfamily)= line.strip("\n").split("\t")
                if regscore in WantedScores:
                    filteredscores.write(line) #chrom + "\t" + start + "\t" + end + "\t" + refAllele + "\t" + altAllele + "\t" + probandGT + "\t" + familyID + "\t" + score + "\t" + alleleFreq + "\n")
		# Coordinates will be 0-based since the input file was 0-based

if __name__ == '__main__':
    main()
            	


    
