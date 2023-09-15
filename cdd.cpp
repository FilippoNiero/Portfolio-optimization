#include <ilcplex/ilocplex.h>
#include <vector>
#include <algorithm>

#include "utils.hpp"

ILOSTLBEGIN

#define DEB(param) std::cout << "test: " << std::string( #param ) << " = " << param << "\n";

void solveForMu0(float mu0, int n, int T, float beta, std::vector<std::vector<float>> const &scenario_returns, std::vector<float> const &expected_returns) {

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
            DEB(tmp);
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

        // cplex.setOut(env.getNullStream()); // Silence console output
        // Optimize the problem and obtain solution.
        if (!cplex.solve()) {
            env.error() << "Failed to optimize LP" << endl;
            throw(-1);
        }

        if (cplex.getStatus() == IloAlgorithm::Optimal) {
            std::cout << "Expected return: " << cplex.getValue(expr_expected_return) << std::endl;

            std::cout << "Optimal Portfolio Weights" << std::endl;
            for (int i = 0; i < n; i++) {
                std::cout << i << " : " << cplex.getValue(weights[i]) << std::endl;
            }

            std::cout << "ETA" << cplex.getValue(eta) << std::endl;
            for (int t = 0; t < T; t++) {
                DEB(cplex.getValue(dp_t[t]));
            }

            for (int t = 0; t < T; t++) {
                DEB(cplex.getValue(dn_t[t]));
            }
            std::cout << "Value: " << cplex.getObjValue() << std::endl;
        }
    }
    catch (...) {
        cerr << "Unknown exception caught" << endl;
    }
    env.end();
}

void solve(string input_file, string output_file, float beta) {
    Instance instance(input_file);
    instance.print();

    // Preprocessing

    std::vector<float> expected_returns = instance.getExpectedReturns();

    float max_expected_return = *max_element(expected_returns.begin(), expected_returns.end());

    for(float mu0 = 0.01; mu0 <= max_expected_return; mu0 += 0.01) {
        solveForMu0(mu0, instance.n, instance.T, beta, instance.scenario_returns, expected_returns);
    }
}

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }
    string input_file = argv[1];

    string output_file = getOutputFileString(input_file);

    for(auto b: BETA_VALUES) {
        solve(input_file, output_file, b);
    }

    return 0;
} // END main

