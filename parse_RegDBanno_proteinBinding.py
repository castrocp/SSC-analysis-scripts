#!/usr/bin/env python3

# Creates a dictionary for RegulomeDB protein binding annotations, with the method|protein|celltype as keys and the number of variants containing each unique annotation as the values

import sys
import pandas

def main():

    anno_file = sys.argv[1]

    bindingDict = {}

    with open (anno_file) as infile:
        for line in infile:
            line = line.strip().split("\t")
            binding_anno = (line[7])
            
            # Annotations are separated by a comma and a space, so I want strip the spaces and split by comma
            # This creates a list of each protein binding annotation for each line
            # Lines without protein binding annotation
            binding_anno = [x.strip() for x in binding_anno.split(",")]
            print(binding_anno)

if __name__ == '__main__':
    main()
