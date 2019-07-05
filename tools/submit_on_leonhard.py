from xml_tools import read_config, get_in_xml
import sys
import os
import subprocess
from pathlib import Path
import git

if __name__ == '__main__':

    repo = git.Repo(search_parent_directories=True)


    import argparse

    parser = argparse.ArgumentParser(description="""
Submits the configuration file leonhard. NOTE: Will run in folder of configuration file!
""")



    parser.add_argument('--alsuqcli_path', type=str, default=os.path.join(repo.working_dir, 'alsvinn_build_folder/alsuqcli/alsuqcli'),
                        help="path to alsuqlci")
    parser.add_argument('--config', type=str, required=True,
                        help="Path to configuration file")
    parser.add_argument('--wait_time', type=int, default=24,
                        help='Wait time in hours')
    parser.add_argument('--multi_sample', type=int, default=1,
                        help='Number of processes to use in the sample direction')
    parser.add_argument('--dry_run', action='store_true',
                        help='Only do a dry run, no actual submission done')
    parser.add_argument('--move_to', type=str,
                        help='Moves the results to another folder after simulation is done')
    parser.add_argument('--base_path', type=str, default=repo.working_dir,
                        help='Base path of this repository')

    args = parser.parse_args()
    configuration_file = args.config

    configuration_path = os.path.abspath(os.path.dirname(configuration_file))

    config = read_config(configuration_file)

    number_of_nodes_per_direction = 1

    total_number_of_nodes = number_of_nodes_per_direction**3*args.multi_sample



    r_command_append = "rusage[ngpus_excl_p=8,mem=8000] span[ptile=8]"

    job_chain = os.path.abspath(configuration_file)
    job_chain = ''.join(ch for ch in job_chain if ch.isalnum() or ch == '_')

    command_to_run = [

        'bsub',
        '-R',
        r_command_append,
        '-W',
        f'{args.wait_time}:00',
        '-n',
        str(total_number_of_nodes),
        '-J',
        job_chain,
        'mpirun',
        '-np',
        str(total_number_of_nodes),
        args.alsuqcli_path,
        '--multi-sample',
        str(args.multi_sample),
        '--multi-x',
        str(number_of_nodes_per_direction),
        '--multi-y',
        str(number_of_nodes_per_direction),
        '--multi-z',
        str(number_of_nodes_per_direction),
        os.path.basename(configuration_file),
    ]






    if args.dry_run:
        command_to_run = ['echo', *command_to_run]

    print(f'working_dir={configuration_path}')
    subprocess.run(command_to_run, check = True, cwd = configuration_path)

    if args.move_to is not None:
        destination_base = os.path.relpath(configuration_path, args.base_path)

        destination_folder = os.path.dirname(os.path.join(args.move_to, destination_base))

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder, exist_ok=True)

        command_to_sync = [
            'bsub',
            '-R',
            'light',
            '-w',
            f'done({job_chain})',
            '-W',
            '120:00',
            'bash',
            os.path.join(repo.working_dir, 'tools/move_and_remove.sh'),
            configuration_path,
            destination_folder
        ]

        if args.dry_run:
            command_to_sync = ['echo', *command_to_sync]

        subprocess.run(command_to_sync, check=True, cwd=configuration_path)
