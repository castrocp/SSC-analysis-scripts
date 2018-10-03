#!/usr/bin/env python3

'''
This script can be used to identify the 5' and 3' UTRs using the GENCODE GTF annotation file.

Not every transcript has the UTR annotations, so it will only identify the ones that are annotated.

If they are annotated, the UTR closer to the start of the transcript is labeled as the 5' UTR, and the one closer to the end labeled 3'
'''

import gzip
import re

infile = "/home/castrocp/GencodeReferences/v19.hg19/gencode.v19.annotation.gtf.gz"
outfile = open("/home/castrocp/GencodeReferences/v19.hg19/gencode.v19.annotation.gtf.UTRs.bed","w")

with gzip.open(infile) as f:

    transcript_dict = {}
    current_transcript = ""
    transcript_start = 0
    transcript_end = 0

    for line in f:
        if not line.startswith("#"):
            #chr1    HAVANA  UTR     65419   65433   .       +       .       gene_id "ENSG00000186092.6_4"; transcript_id "ENST00000641515.2_2"; gene_type "protein_coding"; gene_name "OR4F5"; transcript_type "protein_coding"; transcript_name "RP11-34P13.5-001"; exon_number 1; exon_id "ENSE00003812156.1"; level 2; protein_id "ENSP00000493376.2"; tag "RNA_Seq_supported_partial"; tag "basic"; havana_gene "OTTHUMG00000001094.4_4"; havana_transcript "OTTHUMT00000003223.4_2"; remap_original_location "chr1:+:65419-65433"; remap_status "full_contig";
            chrom, source, feature, start, end, score, strand, phase, annotation = line.split("\t")

            # Will only need this if I want to access transcript ID or gene name later
            #annotation = annotation.split("; ")

            if feature == "transcript":
                transcript_start = start
                transcript_end = end
            
            
            if feature == "UTR":
                region = ""
                if strand == "+":
                    dis_to_start = abs(int(start) - int(transcript_start))
                    dis_to_end = abs(int(start) - int(transcript_end))
                    region = "5_UTR" if dis_to_start < dis_to_end else "3_UTR"
                else:
                    dis_to_start = abs(int(end) - int(transcript_end))
                    dis_to_end = abs(int(end) - int(transcript_start))
                    region = "5_UTR" if dis_to_start < dis_to_end else "3_UTR"

                outfile.write(chrom + "\t" + start + "\t" + end + "\t" + region + "\t" + strand + "\n") 
