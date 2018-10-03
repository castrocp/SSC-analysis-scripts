#!/usr/bin/env python3

import pandas as pd
from scipy.stats import chi2_contingency
from collections import Counter
import sys

proband_variant_file = sys.argv[1]
sibling_variant_file = sys.argv[2]

proband_variants_df = pd.read_csv(proband_variant_file, sep='\t', header=None, names=['Chrom','Start','End','Ref','Alt','FamID','RegDbAnno','RegDbScore'])

sibling_variants_df = pd.read_csv(sibling_variant_file, sep='\t', header=None, names=['Chrom','Start','End','Ref','Alt','FamID','RegDbAnno','RegDbScore'])

print(proband_variants_df)
print(sibling_variants_df)  
