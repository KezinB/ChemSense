import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load the CSV file
file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_3_02_25.csv"  # Change this to your actual file path
df = pd.read_csv(file_path)

# Assuming the first column is 'Time' and the rest are sensor readings
time = df.iloc[:, 0]  # First column as time
sensor_columns = df.columns[1:]  # All sensor columns

# Create subplots for each sensor
plt.figure(figsize=(12, 8))

for i, sensor in enumerate(sensor_columns):
    data = df[sensor]
    
    # Find peaks
    peaks, _ = find_peaks(data, height=np.mean(data))  # Adjust height threshold if needed
    
    # Plot original data
    plt.subplot(len(sensor_columns), 1, i+1)
    plt.plot(time, data, label=sensor)
    plt.plot(time.iloc[peaks], data.iloc[peaks], "ro", label="Peaks")  # Mark peaks
    
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()
