#ifndef UTILS_HPP
#define UTILS_HPP

#include <iostream>
#include <fstream>
#include <vector>
#include <string>


const std::string OUTPUT_DIRECTORY = "out/";
const float BETA_VALUES[] = {0.05,0.1,0.2,0.5,0.9,1};
const float BETA_VALUES_LENGTH = 6;
const bool OUTPUT_VALUES = false;
const bool SINGLE_MU0 = false;
const double TARGET_MU0 = 0.05; // 5 % 


const int TIME_LIMIT = 100; //seconds

float annualReturnToDailyReturn(float annualReturn) {
    // There are approximately 252 trading days in a year
    return float(pow(double(1 + annualReturn), double(1.0/252)) - 1);
}

std::string getOutputFileString(std::string input_file, std::string label) {
    return OUTPUT_DIRECTORY + label + "_" + input_file.substr(input_file.find_last_of("/\\") + 1);
}

template <typename T>
void outputSpaceSeparated(std::vector<T>& v, std::ofstream& output) {
    for(const T& x: v) {
        output << x << " ";
    }
    output << "\n";
}

template <typename T>
void outputKeyValue(const std::string& label, const T& value, std::ofstream& output) {
    output << label << "=" << value << "\n";
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

    std::vector<float> getExpectedReturns() {
        std::vector<float> expected_returns(n); 

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
