#! /bin/bash

python ./scenario_generation.py boot --num_scenarios 10 --file_name ../instances/performance_000010 --random_seed 10
python ./scenario_generation.py boot --num_scenarios 20 --file_name ../instances/performance_000020 --random_seed 20
python ./scenario_generation.py boot --num_scenarios 40 --file_name ../instances/performance_000040 --random_seed 30
python ./scenario_generation.py boot --num_scenarios 80 --file_name ../instances/performance_000080 --random_seed 40
python ./scenario_generation.py boot --num_scenarios 160 --file_name ../instances/performance_000160 --random_seed 50
python ./scenario_generation.py boot --num_scenarios 320 --file_name ../instances/performance_000320 --random_seed 60
python ./scenario_generation.py boot --num_scenarios 640 --file_name ../instances/performance_000640 --random_seed 70
python ./scenario_generation.py boot --num_scenarios 1280 --file_name ../instances/performance_001280 --random_seed 80
python ./scenario_generation.py boot --num_scenarios 2560 --file_name ../instances/performance_002560 --random_seed 90
python ./scenario_generation.py boot --num_scenarios 5120 --file_name ../instances/performance_005120 --random_seed 100
python ./scenario_generation.py boot --num_scenarios 10240 --file_name ../instances/performance_010240 --random_seed 110
python ./scenario_generation.py boot --num_scenarios 20480 --file_name ../instances/performance_020480 --random_seed 120
python ./scenario_generation.py boot --num_scenarios 40960 --file_name ../instances/performance_040960 --random_seed 130
