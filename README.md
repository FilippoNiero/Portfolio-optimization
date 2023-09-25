# Portfolio Optimization

Repository for my thesis "Portfolio Optimization: Comparison between Quadratic and Linear Models". Here you will find all the code to run the simulations, and the scripts used to download and elaborate the data



## Installation
1. Install CPLEX, you can refer to this [guide](https://www.ibm.com/docs/en/icos/22.1.1?topic=cplex-installing)

2. Edit the `makefile` to set your CPLEX installation path 

	```
	INCLUDES = -I/path/to/cplex/cplexXX/include -I/path/to/cplex/concertYY/include

	LIB_DIRS = -Lpath/to/cplex/cplexXX/include -L/path/to/cplex/concertYY/lib/archi/tecture
 	```

3. Install python

4. Use `scripts/scenario_generation.py` to generate a custom instance, or use the `generate_backtest_scenarios.sh` or `generate_performance_scenarios.sh` to create a batch

5. Set your parameters in the `utils.cpp` file

	```
	const std::string OUTPUT_DIRECTORY = "out/";
	const float BETA_VALUES[] = {0.01, 0.1, 0.5};
	const float BETA_VALUES_LENGTH = 3;
	const bool OUTPUT_VALUES = true;
	const bool SINGLE_MU0 = true;
	const double TARGET_MU0 = 0.07; // Annual rate 


	const int TIME_LIMIT = 100; //seconds

	```
6. Run with `make run`

