#include <ilcplex/ilocplex.h>
#include <vector>
#include <algorithm>
#include <chrono>

#include "utils.hpp"

ILOSTLBEGIN

#define DEB(param) std::cout << "test: " << std::string( #param ) << " = " << param << "\n";

void solveForMu0(float mu0, int n, int T, float beta, std::vector<std::vector<float>> const &scenario_returns, std::vector<float> const &expected_returns, std::ofstream& output) {
    auto start_mu0 = std::chrono::high_resolution_clock::now();
    outputKeyValue("mu0", mu0, output);

    float beta_frac = (1.0 - beta) / beta;
    float p = 1.0/T;

    IloEnv env;

    try {
        // Decision variables
        IloNumVarArray weights(env, n, 0.0, 1.0);

        IloModel model(env);

        IloNumVar eta(env);
        model.add(eta);

        IloNumVarArray dp_t(env, T, 0.0, IloInfinity);
        model.add(dp_t);
        IloNumVarArray dn_t(env, T, 0.0, IloInfinity);
        model.add(dn_t);

        for (int t = 0; t < T; t++) {
            IloExpr tmp(env);
            for (int i = 0; i < n; i++) {
                tmp += scenario_returns[i][t] * weights[i];
            }
            model.add(dn_t[t] - dp_t[t] == eta - tmp);
        }

        // Minimize conditionalsemideviation
        IloExpr cdev(env);


        for (int t = 0; t < T; t++) {
            cdev += (dp_t[t] + beta_frac * dn_t[t]) * p;
        }

        model.add(IloMinimize(env, cdev));

        // Budget constraint
        IloExpr total_investment(env);
        for (int i = 0; i < n; i++) {
            total_investment += weights[i];
        }
        model.add(total_investment == 1.0);

        // Expected return constraint
        IloExpr expr_expected_return(env);
        for (int i = 0; i < n; i++) {
            expr_expected_return += expected_returns[i] * weights[i];
        }
        model.add(expr_expected_return >= mu0);

        IloCplex cplex(model);

        cplex.setOut(env.getNullStream()); // Silence console output

        // Optimize the problem and obtain solution.
        if (!cplex.solve()) {
            if (cplex.getStatus() == IloAlgorithm::Infeasible) {
                std::cout << "CDD: CPLEX terminated due to time limit." << std::endl;
                output << "time(us)=INF" << std::endl;
                outputKeyValue("memory(KB)", cplex.getNrows() * 1024 / 1000 , output);
                return;
            } 
            env.error() << "Failed to optimize LP" << endl;
            throw(-1);
        }
        cplex.setParam(IloCplex::Param::TimeLimit, TIME_LIMIT);

        if (cplex.getStatus() == IloAlgorithm::Optimal) {
            // std::cout << "Expected return: " << cplex.getValue(expr_expected_return) << std::endl;
            // std::cout << "ETA" << cplex.getValue(eta) << std::endl;
            // for (int t = 0; t < T; t++) {
            //     DEB(cplex.getValue(dp_t[t]));
            // }

            // for (int t = 0; t < T; t++) {
            //     DEB(cplex.getValue(dn_t[t]));
            // }
            // std::cout << "Value: " << cplex.getObjValue() << std::endl;

            auto end_mu0 = std::chrono::high_resolution_clock::now();

            outputKeyValue("time(us)", chrono::duration_cast<chrono::microseconds>(end_mu0 - start_mu0).count(), output);
            outputKeyValue("memory(KB)", cplex.getNrows() * 1024 / 1000 , output);

            if(OUTPUT_VALUES) {
                output << "solution ";
                
                for (int i = 0; i < n; i++) {
                    output << cplex.getValue(weights[i]) << " ";
                }
                output << '\n';
            }


        }
        

    }
    catch (...) {
        cerr << "Unknown exception caught" << endl;
    }
    env.end();
}

void solve(string input_file, string output_file, float beta) {
    auto start = std::chrono::high_resolution_clock::now();
    cout << "Solving "<< output_file << std::endl;

    Instance instance(input_file);
    std::ofstream output(output_file);

    outputKeyValue("tickers", instance.tickers.size(), output);
    if(OUTPUT_VALUES) outputSpaceSeparated(instance.tickers, output);
    
    output << "cdd beta=" << beta << " " << instance.scenario_returns[0].size() << "\n";
    // Preprocessing
    std::vector<float> expected_returns = instance.getExpectedReturns();

    float max_expected_return = *max_element(expected_returns.begin(), expected_returns.end());

    auto end_precalc = std::chrono::high_resolution_clock::now();
    outputKeyValue("precalc(us)", chrono::duration_cast<chrono::microseconds>(end_precalc - start).count(), output);
    output << std::endl;
    
    for(int i = 1; i <= 100; i++) {    
        solveForMu0(max_expected_return * i / 100, instance.n, instance.T, beta, instance.scenario_returns, expected_returns, output);
        std::cout << i << "/" << 100 << "\n";
        output << std::endl;

    }
    auto end_total_time = std::chrono::high_resolution_clock::now();

    outputKeyValue("total_time(us)", chrono::duration_cast<chrono::microseconds>(end_total_time - start).count(), output);
    std::cout << "Solved "<< output_file << std::endl;

    output.close();

}

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }
    string input_file = argv[1];

    for(int i = 0; i < BETA_VALUES_LENGTH; i++) {
        string output_file = getOutputFileString(input_file, "cdd_beta_" + std::to_string(i));
        solve(input_file, output_file, BETA_VALUES[i]);
    }


    return 0;
} // END main

