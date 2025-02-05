import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

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

    # Find peaks (adjust height threshold, distance, and prominence as needed)
    # peaks, _ = find_peaks(data, height=np.mean(data) + 0.5 * np.std(data), distance=10, prominence=0.8)
    peaks, _ = find_peaks(data, height=np.mean(data) + 0.5 * np.std(data), distance=250)
    # Plot original data
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    plt.plot(time.iloc[peaks], data.iloc[peaks], "ro", label="Peaks")  # Mark peaks
    
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()
