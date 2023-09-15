#include <ilcplex/ilocplex.h>
#include <vector>
#include <algorithm>

#include "utils.hpp"
ILOSTLBEGIN

#define DEB(param) std::cout << "test: " << std::string( #param ) << " = " << param << "\n";

void solveForMu0(float mu0, int n, int T, std::vector<float> const &expected_returns, std::vector<std::vector<float>> const &covariance) {
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

        // Optimize the problem and obtain solution.
        if (!cplex.solve()) {
            env.error() << "Failed to optimize QP" << endl;
            throw(-1);
        }

        if(cplex.getStatus() == IloAlgorithm::Optimal) {
            std::cout << "Optimal Portfolio Weights" << std::endl;
            for(int i = 0; i < n; i++) {
                std::cout << i << " : " << cplex.getValue(weights[i]) << std::endl;
            }
            std::cout << "Variance: " << cplex.getObjValue() << std::endl;
            std::cout << "Expected return: " << cplex.getValue(expr_expected_return) << std::endl;
        }

    }catch (...) {
        cerr << "Unknown exception caught" << endl;
    }

    env.end();

}

void solve(string input_file, string output_file) {
    Instance instance(input_file);
    instance.print();

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
    
    // Print covariance
    for (const std::vector<float>& cov : covariance) {
        for (float c : cov) {
            std::cout << c << ' ';
        }
        std::cout << std::endl;
    }

    // Solve for a specific mu0
    for(float mu0 = 0.01; mu0 <= max_expected_return; mu0 += 0.01) {
        solveForMu0(mu0, instance.n, instance.T, expected_returns, covariance);
    }
}

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }
    string input_file = argv[1];

    string output_file = getOutputFileString(input_file);

    solve(input_file, output_file);

    return 0;
} // END main

