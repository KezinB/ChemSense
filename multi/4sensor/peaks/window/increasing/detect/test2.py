import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file (update the file path as needed)
file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_3_02_25.csv"

# Try different encodings in case of issues
try:
    df = pd.read_csv(file_path, encoding="ISO-8859-1")
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding="latin1")

# Display basic info
print(df.info())

# Drop empty sensor columns (Sensor 6 and Sensor 7)
valid_sensors = df.columns[7:9]  # Assuming first column is "Time"

# Extract time column
time = df["Time"]

# Create subplots for each sensor
plt.figure(figsize=(12, 12))

for i, sensor in enumerate(valid_sensors):
    data = df[sensor]

    increasing_trends = []
    trend_start_indices = []
    trend_end_indices = []
    
    window_size = 5  # You can adjust the window size
    
    for j in range(len(data) - window_size):
        window = data[j:j + window_size]
        if np.all(np.diff(window) > 0):  # Check if all differences are positive
            trend_start_indices.append(j)
            trend_end_indices.append(j + window_size)
            increasing_trends.append(data[j:j + window_size])
    
    upper_values = [max(trend) for trend in increasing_trends]
    lower_values = [min(trend) for trend in increasing_trends]

    # Plot original data and mark upper and lower values of increasing trends
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')

    for start, end, upper, lower in zip(trend_start_indices, trend_end_indices, upper_values, lower_values):
        plt.plot(time.iloc[start:end], data.iloc[start:end], "g", alpha=0.5)  # Highlight increasing trend
        plt.plot(time.iloc[start:end][data.iloc[start:end] == upper], upper, "ro", label="Upper Value" if i == 0 else "")  # Mark upper value
        plt.plot(time.iloc[start:end][data.iloc[start:end] == lower], lower, "go", label="Lower Value" if i == 0 else "")  # Mark lower value

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()
