#!/usr/bin/env python3

'''
This script can be used to identify promoters using the GENCODE GTF annotation file.

The user defined "span" is the number of base pairs from the start of the transcript that is defined as the promoter region
'''

import gzip
import re

infile = "/home/castrocp/GencodeReferences/v19.hg19/gencode.v19.annotation.gtf.gz"
outfile = open("/home/castrocp/GencodeReferences/v19.hg19/gencode.v19.annotation.gtf.promoterss.bed","w")
span = 1000

with gzip.open(infile) as f:


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
                    promoter_end = start
                else:
                    promoter_start = int(end) - int(span)
                    promoter_end = end
            
                # adjust the promoter start coordinate in case it goes negative
                if promoter_start < 0:
                    promoter_start = 0
                
                outfile.write(chrom + "\t" + str(promoter_start) + "\t" + str(promoter_end) + "\t" + strand + "\n") 
