#!/usr/bin/env  python3

import pandas as pd
import mygene 
mg = mygene.MyGeneInfo()

# load the sfari genes and their scores into a data frame
sfari_genes_df = pd.read_csv('/data/data_repo/castrocp/SFARIgenes/SFARI.genes.2-6-19')

# create a subset of this consisting of only genes that score 1,2,3,4,5 and/or S (syndromic)
# the only genes being excluded are those that score a 6, as SFARI defines those as having evidence arguing against a role in autism

sfari_genes_12345S_df = sfari_genes_df.loc[(sfari_genes_df['gene-score']==1.0) | (sfari_genes_df['gene-score']==2.0) | (sfari_genes_df['gene-score']==3.0) | (sfari_genes_df['gene-score']==4.0) | (sfari_genes_df['gene-score']==5.0) | (sfari_genes_df['syndromic']==1)]

# These are all of the genes I will be interested in obtaining entrezIDs for
gene_symbols_12345S = sfari_genes_12345S_df['gene-symbol']

# Fetch the entrez IDs for my genes of interest
entrez_ids_12345S = mg.querymany(gene_symbols_12345S, scopes='symbol', species='human', as_dataframe=True)

# Pull out the column containing the entrezIDs and make a new data frameout of it
entrezID_df = entrez_ids_12345S[['entrezgene']].copy()

# Add a column to the data frame to identify which gene set the entrez IDs belong to
entrezID_df['gene_set'] = 'SFARI_1_2_3_4_5_S'

# Re-order the columsn so the gene set name is the first column
entrezID_df = entrezID_df[['gene_set','entrezgene']]



### ADD OTHER GENE SETS TO THIS DATA FRAME AS SUBSETS WITH DIFFERENT SFARI SCORES
