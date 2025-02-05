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

    # Detect increasing trends
    increasing_trends = []
    upper_values = []
    lower_values = []
    window_size = 25  # You can adjust the window size
    for j in range(len(data) - window_size):
        window = data[j:j + window_size]
        if np.all(np.diff(window) > 0):  # Check if all differences are positive
            mid_point = j + window_size // 2
            increasing_trends.append(mid_point)  # Use the middle point of the window
            upper_values.append(data[mid_point])
            lower_values.append(data[j])

    # Plot original data and mark increasing trends
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    plt.plot(time.iloc[increasing_trends], upper_values, "ro", label="Upper Values")  # Mark upper values
    plt.plot(time.iloc[increasing_trends], lower_values, "go", label="Lower Values")  # Mark lower values
    
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()
