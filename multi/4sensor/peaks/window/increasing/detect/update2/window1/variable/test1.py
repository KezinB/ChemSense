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
valid_sensors = df.columns[7:9]  # Adjust based on actual sensor columns

# Extract time column
time = df["Time"]

# Initialize storage for key points
key_points = {}

# Create subplots for each sensor
plt.figure(figsize=(12, 12))

for i, sensor in enumerate(valid_sensors):
    data = df[sensor]

    # Detect increasing segments
    increasing_segments = []
    segment_indices = []
    
    min_window_size = 15  # Minimum window size for increase detection
    max_window_size = 100  # Maximum window size
    
    j = 0
    while j < len(data) - min_window_size:
        window_size = min_window_size
        while j + window_size < len(data) and window_size <= max_window_size:
            window = data[j:j + window_size]
            if np.all(np.diff(window) > 0):
                window_size += 1
            else:
                break
        if window_size > min_window_size:
            increasing_segments.append(data[j:j + window_size])
            segment_indices.append((j, j + window_size))
        j += window_size  # Move to the next window
    
    # Identify upper (peak) and lower (start) values
    upper_values = [max(segment) for segment in increasing_segments]
    lower_values = [min(segment) for segment in increasing_segments]
    
    # Store key points
    key_points[sensor] = {"Start": [], "Peak": [], "Decrease": [], "Stabilization": []}

    # Plot original data and mark upper and lower values of increasing segments
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    
    for indices, segment, upper, lower in zip(segment_indices, increasing_segments, upper_values, lower_values):
        start, end = indices
        plt.plot(time.iloc[start:end], segment, "g", alpha=0.5)  # Highlight increasing segment
        
        # Find the index of the upper and lower values within the segment
        upper_idx = np.argmax(segment)
        lower_idx = np.argmin(segment)
        
        upper_time = time.iloc[start + upper_idx]
        lower_time = time.iloc[start + lower_idx]
        
        plt.plot(upper_time, upper, "ro", label="Upper Value" if i == 0 else "")  # Mark upper value
        plt.plot(lower_time, lower, "go", label="Lower Value" if i == 0 else "")  # Mark lower value
        
        # Annotate the peaks with time and value
        plt.text(upper_time, upper, f'Time: {upper_time}\nValue: {upper:.5f}', fontsize=9, ha='left', color='red')
        plt.text(lower_time, lower, f'Time: {lower_time}\nValue: {lower:.5f}', fontsize=9, ha='right', color='green')

        # Store key points
        key_points[sensor]["Start"].append((lower_time, lower))
        key_points[sensor]["Peak"].append((upper_time, upper))

    # Different Window Sizes for Decrease and Stabilization
    window_size_decrease = 15  # Controls how fast a decrease is detected
    window_size_stabilize = 30  # Controls how stable the data should be before marking stabilization
    decrease_threshold = -0.0005  # How much the signal must drop to count as a decrease
    stabilization_variation = 0.0002  # Allowed variation for stabilization

    for peak_time, peak_value in key_points[sensor]["Peak"]:
        peak_idx = time[time == peak_time].index[0]

        # Window-based Decrease Detection
        decrease_idx = peak_idx
        for j in range(peak_idx, len(data) - window_size_decrease):
            window = data[j:j + window_size_decrease]
            if np.mean(np.diff(window)) < decrease_threshold:  # Check if window shows a decreasing trend
                decrease_idx = j
                break
        
        decrease_time = time.iloc[decrease_idx]
        decrease_value = data.iloc[decrease_idx]

        # Window-based Stabilization Detection
        stability_idx = decrease_idx
        for j in range(decrease_idx, len(data) - window_size_stabilize):
            window = data[j:j + window_size_stabilize]
            if np.max(window) - np.min(window) < stabilization_variation:  # Check if signal stabilizes
                stability_idx = j
                break

        stability_time = time.iloc[stability_idx]
        stability_value = data.iloc[stability_idx]

        # Plot and annotate decrease and stabilization points
        plt.plot(decrease_time, decrease_value, "bv", label="Decrease" if i == 0 else "")  # Mark decrease
        plt.plot(stability_time, stability_value, "ms", label="Stabilization" if i == 0 else "")  # Mark stabilization
        
        plt.text(decrease_time, decrease_value, f'Time: {decrease_time}\nValue: {decrease_value:.5f}', 
                 fontsize=9, ha='right', color='blue')
        plt.text(stability_time, stability_value, f'Time: {stability_time}\nValue: {stability_value:.5f}', 
                 fontsize=9, ha='left', color='purple')

        # Store key points
        key_points[sensor]["Decrease"].append((decrease_time, decrease_value))
        key_points[sensor]["Stabilization"].append((stability_time, stability_value))

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()

# Print detected key points
for sensor, points in key_points.items():
    print(f"\nKey Points for {sensor}:")
    for point_type, values in points.items():
        print(f"{point_type}: {values}")
