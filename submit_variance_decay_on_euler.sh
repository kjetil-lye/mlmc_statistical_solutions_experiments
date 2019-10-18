#!/bin/bash
set -e
export PYTHONPATH=$(pwd)/python:$PYTHONPATH

function submit() {
    bsub -W 120:00 -R 'rusage[mem=128000]' "$@"
}
module load texlive
datapath='/cluster/work/math/klye/single_sample_structure_functions/'

for order in 1 2
do
    for variable in rho mx my E all;
    do
	for functional in 'identity' 'm2';
	do
	    for time_averaged in '' '_time_integrated';
	    do
		# This looks a bit complicated, but basically, we will use the precomputed
		# m2 functional if we are time integrating, otherwise, we will compute in
		# on line.
		functional_filename='identity'
		functional_to_compute=${functional}
		if [[ "${functional}" == "m2" ]];
		then
		    if [[ "${time_averaged}" == "_time_integrated" ]]
		    then
			functional_filename='moment_2'
			functional_to_compute='identity'
		    fi
		fi

		file_time=1
		if [[ "${time_averaged}" == "_time_integrated" ]]
		then
		    file_time=0
		fi

		time_averaged_title=""

		if [[ "${time_averaged}" == "_time_integrated" ]]
		then
		    time_averaged_title=" time integrated"
		fi
		
		
		submit python python/estimate_variance_decay.py \
		       --input_basename ${datapath}experiments_full_time_average/kh/p0_06/N{resolution}/kh_functional${time_averaged}_${functional_filename}_${file_time}.nc \
		       --starting_resolution 64 \
		       --max_resolution 1024 \
		       --title "Kelvin-Helmholtz \$\epsilon=0.06\$ ${time_averaged_title}" \
		       --variable ${variable} \
		       --norm_order ${order} \
		       --functional ${functional_to_compute}
		
		submit python python/estimate_variance_decay.py \
		       --input_basename ${datapath}experiments_full_time_average/cloudshock/p0_06/N{resolution}/cloudshock_functional${time_averaged}_${functional_filename}_${file_time}.nc \
		       --starting_resolution 64 \
		       --max_resolution 1024 \
		       --title "Cloudshock \$\\epsilon=0.06\$ ${time_averaged_title}" \
		       --variable ${variable} \
		       --norm_order ${order} \
		       --functional ${functional_to_compute}

		submit python python/estimate_variance_decay.py \
		       --input_basename ${datapath}experiments_full_time_average/rm/p0_06/N{resolution}/rm_functional${time_averaged}_${functional_filename}_${file_time}.nc \
		       --starting_resolution 64 \
		       --max_resolution 1024 \
		       --title "Richtmeyer-Meshkov \$\\epsilon=0.06\$ ${time_averaged_title}" \
		       --variable ${variable} \
		       --norm_order ${order} \
		       --functional ${functional_to_compute}
		
		submit python python/estimate_variance_decay.py \
		       --input_basename ${datapath}experiments_full_time_average/shockvortex/p0_06/N{resolution}/shockvortex_functional${time_averaged}_${functional_filename}_${file_time}.nc \
		       --starting_resolution 64 \
		       --max_resolution 1024 \
		       --title "Shockvortex \$\epsilon=0.06\$ ${time_averaged_title}" \
		       --variable ${variable} \
		       --norm_order ${order} \
		       --functional ${functional_to_compute}
		


		for H in 0.125 0.5 0.75
		do
		    submit python python/estimate_variance_decay.py \
			   --input_basename ${datapath}experiments_full_time_average/fbb/H${H//./_}/N{resolution}/euler_fbb_functional${time_averaged}_${functional_filename}_${file_time}.nc \
			   --starting_resolution 64 \
			   --max_resolution 1024 \
			   --title "fBb \$H=${H}\$ ${time_averaged_title}" \
			   --variable ${variable} \
			   --norm_order ${order} \
			   --functional ${functional_to_compute}
		done
	    done
	done
    done
done





