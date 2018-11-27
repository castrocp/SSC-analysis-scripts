#!/bin/bash

# These commands will create files for groups of 75 families from the Phase2and3-1 group. From the files of 75 family IDs, another file containing just the sample IDs for the individuals belonging to those families will be created.


head -150 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_76-150_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_76-150_family_ids.txt > ssc_phase2and3-1_quads_76-150_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_76-150_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_76-150_sample_ids.txt


head -225 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_151-225_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_151-225_family_ids.txt > ssc_phase2and3-1_quads_151-225_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_151-225_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_151-225_sample_ids.txt


head -300 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_226-300_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_226-300_family_ids.txt > ssc_phase2and3-1_quads_226-300_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_226-300_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_226-300_sample_ids.txt


head -375 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_301-375_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_301-375_family_ids.txt > ssc_phase2and3-1_quads_301-375_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_301-375_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_301-375_sample_ids.txt


head -450 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_376-450_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_376-450_family_ids.txt > ssc_phase2and3-1_quads_376-450_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_376-450_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_376-450_sample_ids.txt


head -525 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_451-525_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_451-525_family_ids.txt > ssc_phase2and3-1_quads_451-525_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_451-525_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_451-525_sample_ids.txt


head -600 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_526-600_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_526-600_family_ids.txt > ssc_phase2and3-1_quads_526-600_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_526-600_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_526-600_sample_ids.txt


head -675 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_601-675_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_601-675_family_ids.txt > ssc_phase2and3-1_quads_601-675_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_601-675_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_601-675_sample_ids.txt


head -750 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_676-750_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_676-750_family_ids.txt > ssc_phase2and3-1_quads_676-750_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_676-750_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_676-750_sample_ids.txt


head -825 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_751-825_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_751-825_family_ids.txt > ssc_phase2and3-1_quads_751-825_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_751-825_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_751-825_sample_ids.txt


head -900 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_826-900_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_826-900_family_ids.txt > ssc_phase2and3-1_quads_826-900_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_826-900_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_826-900_sample_ids.txt


head -975 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_901-975_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_901-975_family_ids.txt > ssc_phase2and3-1_quads_901-975_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_901-975_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_901-975_sample_ids.txt


head -1050 ssc_phase2and3-1_quads_family_ids.txt | tail -75 > ssc_phase2and3-1_quads_976-1050_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_976-1050_family_ids.txt > ssc_phase2and3-1_quads_976-1050_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_976-1050_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_976-1050_sample_ids.txt


head -1132 ssc_phase2and3-1_quads_family_ids.txt | tail -82 > ssc_phase2and3-1_quads_1051-1132_family_ids.txt

awk '{print $1"."}' ssc_phase2and3-1_quads_1051-1132_family_ids.txt > ssc_phase2and3-1_quads_1051-1132_family_ids_withPeriod.txt

grep -Ff ssc_phase2and3-1_quads_1051-1132_family_ids_withPeriod.txt ssc_phase2and3-1_quads_id_mapping.txt | awk '{print $2}' > ssc_phase2and3-1_quads_1051-1132_sample_ids.txt
