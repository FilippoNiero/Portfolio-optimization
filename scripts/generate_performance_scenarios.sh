#! /bin/bash

python ./scenario_generation.py boot --num_scenarios 10 --file_name ../instances/performance_000010
python ./scenario_generation.py boot --num_scenarios 20 --file_name ../instances/performance_000020
python ./scenario_generation.py boot --num_scenarios 40 --file_name ../instances/performance_000040
python ./scenario_generation.py boot --num_scenarios 80 --file_name ../instances/performance_000080
python ./scenario_generation.py boot --num_scenarios 160 --file_name ../instances/performance_000160
python ./scenario_generation.py boot --num_scenarios 320 --file_name ../instances/performance_000320
python ./scenario_generation.py boot --num_scenarios 640 --file_name ../instances/performance_000640
python ./scenario_generation.py boot --num_scenarios 1280 --file_name ../instances/performance_001280
python ./scenario_generation.py boot --num_scenarios 2560 --file_name ../instances/performance_002560
python ./scenario_generation.py boot --num_scenarios 5120 --file_name ../instances/performance_005120
python ./scenario_generation.py boot --num_scenarios 10240 --file_name ../instances/performance_010240
python ./scenario_generation.py boot --num_scenarios 20480 --file_name ../instances/performance_020480
python ./scenario_generation.py boot --num_scenarios 40960 --file_name ../instances/performance_040960
