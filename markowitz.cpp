#include <ilcplex/ilocplex.h>
#include <vector>
#include <algorithm>
#include <chrono>


#include "utils.hpp"
ILOSTLBEGIN

#define DEB(param) std::cout << "test: " << std::string( #param ) << " = " << param << "\n";

void solveForMu0(float mu0, int n, int T, std::vector<float> const &expected_returns, std::vector<std::vector<float>> const &covariance, std::ofstream& output) {
    auto start_mu0 = std::chrono::high_resolution_clock::now();
    outputKeyValue("mu0", mu0, output);
    
    IloEnv env;

    try {
        //Decision variables
        IloNumVarArray weights(env, n, 0.0, 1.0);

        IloModel model(env);
        
    
        //Minimize variance
        IloExpr risk(env);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                risk += covariance[i][j] * weights[i] * weights[j];
            }
        }

        model.add(IloMinimize(env, risk));
        
        //Budget constraint
        IloExpr total_investment(env);
        for (int i = 0; i < n; i++) {
            total_investment += weights[i];
        }
        model.add(total_investment == 1.0);

        //Expected return constraint
        IloExpr expr_expected_return(env);
        for (int i = 0; i < n; i++) {
            expr_expected_return += expected_returns[i] * weights[i];
        }
        model.add(expr_expected_return >= mu0);
            
        IloCplex cplex(model);
        
        cplex.setOut(env.getNullStream()); // Silence console output
        cplex.setWarning(env.getNullStream()); // Silence diagonal perturbation warning
        
        cplex.setParam(IloCplex::Param::TimeLimit, TIME_LIMIT);

        // Optimize the problem and obtain solution.
        if (!cplex.solve()) {
            if (cplex.getStatus() == IloAlgorithm::Infeasible) {
                std::cout << "Markowitz: CPLEX terminated due to time limit." << std::endl;
                output << "time(us)=INF" << std::endl;
                outputKeyValue("memory(KB)", cplex.getNrows() * 1024 / 1000 , output);
                return;
            } 
            env.error() << "Failed to optimize QP" << endl;
            throw(-1);
        }


        if(cplex.getStatus() == IloAlgorithm::Optimal) {
            // std::cout << "Optimal Portfolio Weights" << std::endl;
            // for(int i = 0; i < n; i++) {
            //     std::cout << i << " : " << cplex.getValue(weights[i]) << std::endl;
            // }
            // std::cout << "Variance: " << cplex.getObjValue() << std::endl;
            // std::cout << "Expected return: " << cplex.getValue(expr_expected_return) << std::endl;

            auto end_mu0 = std::chrono::high_resolution_clock::now();

            outputKeyValue("time(us)", chrono::duration_cast<chrono::microseconds>(end_mu0 - start_mu0).count(), output);
            outputKeyValue("memory(KB)", (cplex.getNrows() + cplex.getNcols() * cplex.getNcols()) * 1024 / 1000, output);
            if(OUTPUT_VALUES) {
                output << "solution ";
                
                for (int i = 0; i < n; i++) {
                    output << cplex.getValue(weights[i]) << " ";
                }
                output << '\n';
            }
        }

    }catch (...) {
        cerr << "Unknown exception caught" << endl;
    }

    env.end();

}

void solve(string input_file, string output_file) {
    auto start = std::chrono::high_resolution_clock::now();

    cout << "Markowitz: solving "<< output_file << std::endl;
    Instance instance(input_file);
    std::ofstream output(output_file);

    outputKeyValue("tickers", instance.tickers.size(), output);
    if(OUTPUT_VALUES) outputSpaceSeparated(instance.tickers, output);

    output << "markowitz " << instance.scenario_returns[0].size() << "\n";

    // Preprocessing
    
    std::vector<float> expected_returns = instance.getExpectedReturns();

    float max_expected_return = *max_element(expected_returns.begin(), expected_returns.end());

    // Calculate covariance
    std::vector<std::vector<float> > covariance(instance.n);

    for(int i = 0; i < instance.n; i++) {
        covariance[i] = std::vector<float>(instance.n);
        for(int j = 0; j < instance.n; j++) {
            float acc = 0;
            for(int t = 0; t < instance.T; t++) {
                acc += (instance.scenario_returns[i][t] - expected_returns[i]) * (instance.scenario_returns[j][t] - expected_returns[j]);
            }
            covariance[i][j] = acc / instance.T;
        }    
    }
    auto end_precalc = std::chrono::high_resolution_clock::now();
    outputKeyValue("precalc(us)", chrono::duration_cast<chrono::microseconds>(end_precalc - start).count(), output);
    output << std::endl;

    // // Print covariance
    // for (const std::vector<float>& cov : covariance) {
    //     for (float c : cov) {
    //         std::cout << c << ' ';
    //     }
    //     std::cout << std::endl;
    // }

    // Solve for a specific mu0
    if(SINGLE_MU0) {
        solveForMu0(annualReturnToDailyReturn(TARGET_MU0), instance.n, instance.T, expected_returns, covariance, output);
    }else {
        for(int i = 1; i <= 100; i++) {
            solveForMu0(max_expected_return * i / 100 , instance.n, instance.T, expected_returns, covariance, output);
            std::cout << i << "/" << 100 << "\n";
            output << std::endl;
        }
    }
    auto end_total_time = std::chrono::high_resolution_clock::now();

    outputKeyValue("total_time(us)", chrono::duration_cast<chrono::microseconds>(end_total_time - start).count(), output);
    std::cout << "Markowitz: solved "<< output_file << std::endl;
    output.close();

}

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }
    string input_file = argv[1];

    string output_file = getOutputFileString(input_file, "markowitz");

    solve(input_file, output_file);

    return 0;
} // END main

