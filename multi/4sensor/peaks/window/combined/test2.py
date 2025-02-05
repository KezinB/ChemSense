import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file (update the file path as needed)
file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_3_02_25.csv"
# file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_final.csv"

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
    
    increasing_segments = []
    decreasing_segments = []
    segment_indices_inc = []
    segment_indices_dec = []
    
    # Define different window sizes for increasing and decreasing segments
    min_window_size_inc = 15
    max_window_size_inc = 100
    min_window_size_dec = 20
    max_window_size_dec = 80
    
    j = 0
    while j < len(data) - min_window_size_inc:
        window_size = min_window_size_inc
        while j + window_size < len(data) and window_size <= max_window_size_inc:
            window = data[j:j + window_size]
            if np.all(np.diff(window) > 0):
                window_size += 1
            else:
                break
        if window_size > min_window_size_inc:
            increasing_segments.append(data[j:j + window_size])
            segment_indices_inc.append((j, j + window_size))
        j += window_size  # Move to the next window
    
    k = 0
    while k < len(data) - min_window_size_dec:
        window_size = min_window_size_dec
        while k + window_size < len(data) and window_size <= max_window_size_dec:
            window = data[k:k + window_size]
            if np.all(np.diff(window) < 0):
                window_size += 1
            else:
                break
        if window_size > min_window_size_dec:
            decreasing_segments.append(data[k:k + window_size])
            segment_indices_dec.append((k, k + window_size))
        k += window_size  # Move to the next window
    
    upper_values_inc = [max(segment) for segment in increasing_segments]
    lower_values_inc = [min(segment) for segment in increasing_segments]
    upper_values_dec = [max(segment) for segment in decreasing_segments]
    lower_values_dec = [min(segment) for segment in decreasing_segments]

    # Plot original data and mark upper and lower values of increasing and decreasing segments
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    
    for indices, segment, upper, lower in zip(segment_indices_inc, increasing_segments, upper_values_inc, lower_values_inc):
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
    
    for indices, segment, upper, lower in zip(segment_indices_dec, decreasing_segments, upper_values_dec, lower_values_dec):
        start, end = indices
        plt.plot(time.iloc[start:end], segment, "r", alpha=0.5)  # Highlight decreasing segment
        
        # Find the index of the upper and lower values within the segment
        upper_idx = np.argmax(segment)
        lower_idx = np.argmin(segment)
        
        upper_time = time.iloc[start + upper_idx]
        lower_time = time.iloc[start + lower_idx]
        
        plt.plot(upper_time, upper, "ro", label="Upper Value (Decreasing)" if i == 0 else "")  # Mark upper value
        plt.plot(lower_time, lower, "go", label="Lower Value (Decreasing)" if i == 0 else "")  # Mark lower value
        
        # Annotate the peaks with time and value
        plt.text(upper_time, upper, f'Time: {upper_time}\nValue: {upper:.5f}', fontsize=9, ha='left', color='red')
        plt.text(lower_time, lower, f'Time: {lower_time}\nValue: {lower:.5f}', fontsize=9, ha='right', color='green')

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()
