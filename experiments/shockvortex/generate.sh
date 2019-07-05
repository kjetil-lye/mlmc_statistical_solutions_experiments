#!/bin/bash
set -e
max_resolution=2048
min_resolution=32
samples=""
sum=0
resolution=$max_resolution
resolutions=""
sample_starts=""
sample_start=0
sample=0
while [[ $resolution -ge $min_resolution ]];
do
    
    echo $resolution
    sample=$((${max_resolution}/${resolution}*${max_resolution} + $sample))
    samples="$sample $samples"
    

    resolutions="$resolution $resolutions"
    resolution=$(($resolution/2))

    sample_starts="$sample_start $sample_starts"

    if [[ $resolution -lt $(($max_resolution/2)) ]]
    then
        sample_start=$(($sample_start+$sample))
    fi
done
echo $samples
echo $sample_starts

python ../../tools/make_resolutions_perturbations.py \
       --config template/shockvortex.xml \
       --resolutions $resolutions \
       --samples $samples \
       --perturbations 0.03 \
       --sample_starts $sample_starts

