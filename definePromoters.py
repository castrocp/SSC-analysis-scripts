#!/usr/bin/env python3

'''
This script can be used to identify promoters using the GENCODE GTF annotation file.

The user defined "span" is the number of base pairs from the start of the transcript that is defined as the promoter region
'''

import gzip
import re

infile = "/home/castrocp/GencodeReferences/v19.hg19/gencode.v19.annotation.gtf.gz"
span = 1500
outfile = open("/home/castrocp/GencodeReferences/v19.hg19/gencode.v19.annotation.gtf.promoters." + str(span) + "bp_upstream.bed","w")

with gzip.open(infile, mode='rt') as f:
# 'rt' opens the file in text mode, which reads characters as strings instead of bytes, since we're opening a gzipped file

    for line in f:
        if not line.startswith("#"):
            #chr1    HAVANA  UTR     65419   65433   .       +       .       gene_id "ENSG00000186092.6_4"; transcript_id "ENST00000641515.2_2"; gene_type "protein_coding"; gene_name "OR4F5"; transcript_type "protein_coding"; transcript_name "RP11-34P13.5-001"; exon_number 1; exon_id "ENSE00003812156.1"; level 2; protein_id "ENSP00000493376.2"; tag "RNA_Seq_supported_partial"; tag "basic"; havana_gene "OTTHUMG00000001094.4_4"; havana_transcript "OTTHUMT00000003223.4_2"; remap_original_location "chr1:+:65419-65433"; remap_status "full_contig";
            chrom, source, feature, start, end, score, strand, phase, annotation = line.split("\t")

            # Will only need this if I want to access transcript ID or gene name later
            #annotation = annotation.split("; ")
            
            promoter_start = ""
            promoter_end = ""
            
            if feature == "transcript":
                if strand == "+":
                    promoter_start = int(start) - int(span)
                    promoter_end = int(start) - 1
                
                    if promoter_start < 0:
                        promoter_start = 0
                    #convert to zero-based for BED format
                    outfile.write(chrom + "\t" + str(promoter_start-1) + "\t" + str(promoter_end-1) + "\t" + strand + "\n")

                else:
                    promoter_start = int(end) + int(span)
                    promoter_end = int(end) + 1
            
                    # adjust the promoter start coordinate in case it goes negative
                    if promoter_start < 0:
                        promoter_start = 0
                
                    #convert to zero-based for BED format. Print from end to start to account for reverse-strand.
                    outfile.write(chrom + "\t" + str(promoter_end-1) + "\t" + str(promoter_start-1) + "\t" + strand + "\n") 
