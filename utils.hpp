#ifndef UTILS_HPP
#define UTILS_HPP

#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

const string OUTPUT_DIRECTORY = "out/";
const float BETA_VALUES[] = {0.0, 0.5, 1.0};

string getOutputFileString(string input_file) {
    return OUTPUT_DIRECTORY + input_file.substr(input_file.find_last_of("/\\") + 1);
}


class Instance {
public:
    int n, T;
    std::vector<std::string> tickers;
    std::vector<std::vector<float>> scenario_returns;

    Instance(const std::string& filename) {
        std::ifstream input(filename);

        if (!input.is_open()) {
            std::cerr << "Could not open the input file." << std::endl;
        }

        input >> n >> T;

        tickers.reserve(n);
        scenario_returns.reserve(n);

        for (int i = 0; i < n; i++) {
            std::string ticker;
            input >> ticker;
            tickers.push_back(ticker);

            std::vector<float> returns(T);
            for (int j = 0; j < T; ++j) {
                input >> returns[j];
            }
            scenario_returns.push_back(returns);
        }

        input.close();
    }

    void print() {
        std::cout << "Tickers:" << std::endl;
        for (const std::string& ticker : tickers) {
            std::cout << ticker << std::endl;
        }

        std::cout << "Scenario Returns:" << std::endl;
        for (const std::vector<float>& returns : scenario_returns) {
            for (float ret : returns) {
                std::cout << ret << ' ';
            }
            std::cout << std::endl;
        }
    }

    vector<float> getExpectedReturns() {
        vector<float> expected_returns(n); 

        for (int i = 0; i < n; i++) {
            float acc = 0;
            for (auto x : scenario_returns[i]) {
                acc += x;
            }
            expected_returns[i] = acc / T; 
        }

        return expected_returns;
    }

    
};



#endif  // UTILS_HPP
