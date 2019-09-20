#!/bin/bash
set -e
export PYTHONPATH=$(pwd)/python:$PYTHONPATH

function submit() {
    bsub -N -B -W 120:00 -R 'rusage[mem=128000]' "$@"
}

for variable in rho mx my E all;
do
    submit python python/estimate_variance_decay.py \
	--input_basename /cluster/work/math/klye/single_sample_structure_functions/experiments_mean_field/kh/p0_06/N{resolution}/kh_1.nc \
	--starting_resolution 64 \
	--max_resolution 1024 \
	--title 'Kelvin-Helmholtz $\epsilon=0.06$' \
	--variable ${variable}

    submit python python/estimate_variance_decay.py \
	--input_basename /cluster/work/math/klye/single_sample_structure_functions/experiments_mean_field/cloudshock/p0_03125/N{resolution}/cloudshock_1.nc \
	--starting_resolution 64 \
	--max_resolution 1024 \
	--title 'Cloudshock $\epsilon=1/32$' \
	--variable ${variable}

    submit python python/estimate_variance_decay.py \
	--input_basename /cluster/work/math/klye/single_sample_structure_functions/experiments_mean_field/rm/p0_06/N{resolution}/rm_1.nc \
	--starting_resolution 64 \
	--max_resolution 1024 \
	--title 'Richtmeyer-Meshkov $\epsilon=0.06$' \
	--variable ${variable}

    submit python python/estimate_variance_decay.py \
	--input_basename /cluster/work/math/klye/single_sample_structure_functions/experiments_mean_field/shockvortex/p0_06/N{resolution}/shockvortex_1.nc \
	--starting_resolution 64 \
	--max_resolution 1024 \
	--title 'Shockvortex $\epsilon=0.06$' \
	--variable ${variable}
    

    submit python python/estimate_variance_decay.py \
	--input_basename /cluster/work/math/klye/single_sample_structure_functions/experiments_mean_field/kh/p0_06/N{resolution}/kh_1.nc \
	--starting_resolution 64 \
	--max_resolution 1024 \
	--title 'Kelvin-Helmholtz $\epsilon=0.06$' \
	--variable ${variable}

    for H in 0.125 0.5 0.75
    do
	submit python python/estimate_variance_decay.py \
	    --input_basename /cluster/work/math/klye/single_sample_structure_functions/experiments_mean_field/fbb/H${H//./_}/N{resolution}/euler_fbb_1.nc \
	    --starting_resolution 64 \
	    --max_resolution 1024 \
	    --title "fBb \$H=${H}\$" \
	    --variable ${variable}
    done
done





