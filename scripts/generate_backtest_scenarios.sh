#! /bin/bash

python3 scenario_generation.py boot --num_scenarios 2500 --end_date 2020-06-15 --file_name ../instances/boot15062022 --random_seed 2
python3 scenario_generation.py block --num_scenarios 2500 --end_date 2020-06-15 --file_name ../instances/block15062022 --block_size 5 --random_seed 17
python3 scenario_generation.py boot --num_scenarios 2500 --end_date 2020-01-01 --file_name ../instances/boot01012020 --random_seed 7
python3 scenario_generation.py block --num_scenarios 2500 --end_date 2020-01-01 --file_name ../instances/block01012020 --block_size 4 --random_seed 23