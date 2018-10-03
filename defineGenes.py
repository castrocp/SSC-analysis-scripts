#!/usr/bin/env python3

'''
This script can be used to identify gene coordinates using the GENCODE GTF annotation file.
'''

import gzip
import re

infile = "/home/castrocp/GencodeReferences/v19.hg19/gencode.v19.annotation.gtf.gz"
outfile = open("/home/castrocp/GencodeReferences/v19.hg19/gencode.v19.annotation.gtf.genes.bed","w")

with gzip.open(infile) as f:
    for line in f:
        if not line.startswith("#"):
            # chr1    HAVANA  gene    11869   14412   .       +       .       gene_id "ENSG00000223972.4"; transcript_id "ENSG00000223972.4"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1"; level 2; havana_gene "OTTHUMG00000000961.2";
            chrom, source, feature, start, end, score, strand, phase, annotation = line.split("\t")
            
            annotation_list= []
            annotation_list = annotation.split("; ")
            for a in annotation_list:
                if a.startswith("gene_name"):
                    gene = a.split(" ")[1]
                    
                    outfile.write(chrom + "\t" + start + "\t" + end + "\t" + gene + "\n") 
