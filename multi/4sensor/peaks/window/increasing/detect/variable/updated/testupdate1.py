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
    
    # Find peaks (upper max) and valleys (lower min)
    peaks, _ = find_peaks(data, height=np.mean(data), distance=20)  # Adjust distance as needed
    valleys, _ = find_peaks(-data, height=np.mean(-data), distance=20)  # Invert data for valleys
    
    # Combine peaks and valleys and sort them
    critical_points = np.sort(np.concatenate((peaks, valleys)))
    
    # Identify segments between critical points
    segments = []
    for j in range(len(critical_points) - 1):
        start = critical_points[j]
        end = critical_points[j + 1]
        segment = data[start:end]
        segments.append((start, end, segment))
    
    # Plot original data
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    
    # Annotate peaks and valleys
    plt.plot(time.iloc[peaks], data.iloc[peaks], "ro", label="Upper Max")  # Upper max
    plt.plot(time.iloc[valleys], data.iloc[valleys], "go", label="Lower Min")  # Lower min
    
    # Label each segment with a number
    for idx, (start, end, segment) in enumerate(segments):
        mid_point = start + (end - start) // 2
        plt.text(time.iloc[mid_point], data.iloc[mid_point], f'{idx + 1}', fontsize=12, ha='center', color='purple')
        
        # Find upper min and lower max within the segment
        upper_min = np.min(segment[segment > np.mean(segment)])  # Upper min
        lower_max = np.max(segment[segment < np.mean(segment)])  # Lower max
        
        # Find indices of upper min and lower max
        upper_min_idx = start + np.argmin(segment[segment > np.mean(segment)])
        lower_max_idx = start + np.argmax(segment[segment < np.mean(segment)])
        
        # Plot upper min and lower max
        plt.plot(time.iloc[upper_min_idx], upper_min, "yx", label="Upper Min" if idx == 0 else "")  # Upper min
        plt.plot(time.iloc[lower_max_idx], lower_max, "bx", label="Lower Max" if idx == 0 else "")  # Lower max
        
        # Annotate upper min and lower max
        plt.text(time.iloc[upper_min_idx], upper_min, f'Upper Min: {upper_min:.5f}', fontsize=9, ha='left', color='orange')
        plt.text(time.iloc[lower_max_idx], lower_max, f'Lower Max: {lower_max:.5f}', fontsize=9, ha='right', color='blue')

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()