#!/bin/bash
#set -e
export PYTHONPATH=$(pwd)/python:$PYTHONPATH

function submit() {
    "$@"
}

for p in 1 2 3
do
    for order in 2
    do
	for variable in rho mx my E all;
	do
	    submit python python/estimate_variance_decay.py \
		   --input_basename single_sample_structure_functions/experiments_multiple_samples/kh/p0_06/N{resolution}/kh_functional_structure_cube_${p}_8.nc \
		   --starting_resolution 64 \
		   --max_resolution 1024 \
		   --title 'Kelvin-Helmholtz $\epsilon=0.06$' \
		   --variable ${variable} \
		   --norm_order ${order} \
		   --structure \
		   --power ${p}
	    
	    submit python python/estimate_variance_decay.py \
		   --input_basename single_sample_structure_functions/experiments_multiple_samples/cloudshock/p0_03125/N{resolution}/cloudshock_functional_structure_cube_${p}_8.nc \
		   --starting_resolution 64 \
		   --max_resolution 1024 \
		   --title 'Cloudshock $\epsilon=1/32$' \
		   --variable ${variable} \
		   --norm_order ${order} \
		   --structure \
		   --power ${p}

	    # submit python python/estimate_variance_decay.py \
	    # 	   --input_basename single_sample_structure_functions/experiments_multiple_samples/rm/p0_06/N{resolution}/rm_functional_structure_cube_${p}_8.nc \
	    # 	   --starting_resolution 64 \
	    # 	   --max_resolution 1024 \
	    # 	   --title 'Richtmeyer-Meshkov $\epsilon=0.06$' \
	    # 	   --variable ${variable} \
	    # 	   --norm_order ${order} \
	    # 	   --structure \
	    # 	   --power ${p}
	    
	    submit python python/estimate_variance_decay.py \
		   --input_basename single_sample_structure_functions/experiments_multiple_samples/shockvortex/p0_06/N{resolution}/shockvortex_functional_structure_cube_${p}_8.nc \
		   --starting_resolution 64 \
		   --max_resolution 1024 \
		   --title 'Shockvortex $\epsilon=0.06$' \
		   --variable ${variable} \
		   --norm_order ${order} \
		   --structure \
		   --power ${p}
	    

	    for H in 0.125 0.5 0.75
	    do
		submit python python/estimate_variance_decay.py \
		       --input_basename single_sample_structure_functions/experiments_multiple_samples/fbb/H${H//./_}/N{resolution}/euler_fbb_functional_structure_cube_${p}_8.nc \
		       --starting_resolution 64 \
		       --max_resolution 1024 \
		       --title "fBb \$H=${H}\$" \
		       --variable ${variable} \
		       --norm_order ${order} \
		       --structure \
		       --power ${p}
	    done
	done
    done
done




