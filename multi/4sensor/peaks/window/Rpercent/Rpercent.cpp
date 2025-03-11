#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <limits>
#include <algorithm>

using namespace std;

// Function to read CSV file into a vector of vectors
vector<vector<string>> readCSV(const string &filename)
{
    ifstream file(filename);
    vector<vector<string>> data;
    string line;

    if (!file.is_open())
    {
        cerr << "Error: Could not open file " << filename << endl;
        return data;
    }

    while (getline(file, line))
    {
        stringstream ss(line);
        string value;
        vector<string> row;
        while (getline(ss, value, ','))
        {
            row.push_back(value);
        }
        data.push_back(row);
    }

    file.close();
    return data;
}

// Function to convert a column from string to double
vector<double> getColumnData(const vector<vector<string>> &data, int colIndex)
{
    vector<double> column;
    for (size_t i = 1; i < data.size(); ++i)
    { // Skipping header
        try
        {
            column.push_back(stod(data[i][colIndex]));
        }
        catch (const exception &)
        {
            column.push_back(numeric_limits<double>::quiet_NaN()); // Handle invalid data
        }
    }
    return column;
}

// Function to detect increasing segments and calculate R%
void detectIncreasingSegments(const vector<double> &data, const vector<double> &time, const string &sensorName)
{
    vector<vector<double>> increasing_segments;
    vector<pair<int, int>> segment_indices;

    int min_window_size = 15;
    int max_window_size = 100;

    size_t j = 0;
    while (j < data.size() - min_window_size)
    {
        int window_size = min_window_size;
        while (j + window_size < data.size() && window_size <= max_window_size)
        {
            bool increasing = true;
            for (int k = 1; k < window_size; ++k)
            {
                if (data[j + k] <= data[j + k - 1])
                {
                    increasing = false;
                    break;
                }
            }
            if (increasing)
            {
                window_size++;
            }
            else
            {
                break;
            }
        }
        if (window_size > min_window_size)
        {
            vector<double> segment(data.begin() + j, data.begin() + j + window_size);
            increasing_segments.push_back(segment);
            segment_indices.emplace_back(j, j + window_size);
        }
        j += window_size;
    }

    // Print detected values
    cout << "Sensor: " << sensorName << endl;
    for (size_t i = 0; i < increasing_segments.size(); ++i)
    {
        double upper = *max_element(increasing_segments[i].begin(), increasing_segments[i].end());
        double lower = *min_element(increasing_segments[i].begin(), increasing_segments[i].end());
        double R_percent = ((upper - lower) / lower) * 100.0;

        int upper_idx = distance(increasing_segments[i].begin(), max_element(increasing_segments[i].begin(), increasing_segments[i].end()));
        int lower_idx = distance(increasing_segments[i].begin(), min_element(increasing_segments[i].begin(), increasing_segments[i].end()));

        int startIdx = segment_indices[i].first;
        double upper_time = time[startIdx + upper_idx];
        double lower_time = time[startIdx + lower_idx];

        cout << "Peak " << i + 1 << ":" << endl;
        cout << "  - Max Value: " << upper << " at Time: " << upper_time << endl;
        cout << "  - Min Value: " << lower << " at Time: " << lower_time << endl;
        cout << "  - R%: " << R_percent << "%" << endl;
        cout << endl;
    }
}

int main()
{
    string file_path = "C:/Users/kezin/OneDrive/Documents/Accubits/Programs/multi/4sensor/peaks/test_final.csv";
    vector<vector<string>> data = readCSV(file_path);

    if (data.empty())
    {
        cerr << "Error: No data found in the CSV file." << endl;
        return 1;
    }

    vector<double> time = getColumnData(data, 0); // Assuming first column is time

    // Process multiple sensors (equivalent to Python's df.columns[7:9])
    vector<int> sensorColumns = {7, 8}; // Modify as needed for actual sensor indices
    for (int colIndex : sensorColumns)
    {
        vector<double> sensorData = getColumnData(data, colIndex);
        string sensorName = data[0][colIndex]; // Assuming first row contains headers
        detectIncreasingSegments(sensorData, time, sensorName);
    }

    return 0;
}
