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

    # Detect decreasing trends
    decreasing_trends = []
    # window_size = 5  # You can adjust the window size
    window_size = 6
    for j in range(len(data) - window_size):
        window = data[j:j + window_size]
        if np.all(np.diff(window) < 0):  # Check if all differences are negative
            decreasing_trends.append(j + window_size // 2)  # Use the middle point of the window

    # Plot original data and mark decreasing trends
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    plt.plot(time.iloc[decreasing_trends], data.iloc[decreasing_trends], "ro", label="Decreasing Trends")  # Mark decreasing trends
    
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()
