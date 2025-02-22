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

# Plot for upper peaks
plt.figure(figsize=(12, 12))
for i, sensor in enumerate(valid_sensors):
    data = df[sensor]
    
    increasing_segments = []
    segment_indices = []
    
    min_window_size_upper = 15  # Minimum window size for upper peaks
    max_window_size_upper = 100  # Maximum window size for upper peaks
    
    j = 0
    while j < len(data) - min_window_size_upper:
        window_size = min_window_size_upper
        while j + window_size < len(data) and window_size <= max_window_size_upper:
            window = data[j:j + window_size]
            if np.all(np.diff(window) > 0):
                window_size += 1
            else:
                break
        if window_size > min_window_size_upper:
            increasing_segments.append(data[j:j + window_size])
            segment_indices.append((j, j + window_size))
        j += window_size  # Move to the next window
    
    upper_values = [max(segment) for segment in increasing_segments]

    # Plot original data and mark upper values of increasing segments
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    
    for idx, (indices, segment, upper) in enumerate(zip(segment_indices, increasing_segments, upper_values)):
        start, end = indices
        plt.plot(time.iloc[start:end], segment, "g", alpha=0.5)  # Highlight increasing segment
        
        upper_idx = np.argmax(segment)
        upper_time = time.iloc[start + upper_idx]
        
        peak_label = f'P{idx+1}'  # Peak label (e.g., P1, P2, P3, ...)
        
        plt.plot(upper_time, upper, "ro", label="Upper Value" if idx == 0 else "")  # Mark upper value
        
        plt.text(upper_time, upper, f'{peak_label}\nTime: {upper_time}\nValue: {upper:.5f}', fontsize=9, ha='left', color='black')

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor} (Upper Peaks)")
    plt.legend()

    # Print the number of upper peaks
    print(f"Number of upper peaks for {sensor}: {len(upper_values)}")

plt.tight_layout()
plt.show()

# Plot for lower peaks
plt.figure(figsize=(12, 12))
for i, sensor in enumerate(valid_sensors):
    data = df[sensor]
    
    decreasing_segments = []
    segment_indices = []
    
    min_window_size_lower = 70  # Minimum window size for lower peaks
    max_window_size_lower = 200  # Maximum window size for lower peaks
    
    j = 0
    while j < len(data) - min_window_size_lower:
        window_size = min_window_size_lower
        while j + window_size < len(data) and window_size <= max_window_size_lower:
            window = data[j:j + window_size]
            if np.all(np.diff(window) < 0):
                window_size += 1
            else:
                break
        if window_size > min_window_size_lower:
            decreasing_segments.append(data[j:j + window_size])
            segment_indices.append((j, j + window_size))
        j += window_size  # Move to the next window
    
    lower_values = [min(segment) for segment in decreasing_segments]

    # Plot original data and mark lower values of decreasing segments
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    
    for idx, (indices, segment, lower) in enumerate(zip(segment_indices, decreasing_segments, lower_values)):
        start, end = indices
        plt.plot(time.iloc[start:end], segment, "r", alpha=0.5)  # Highlight decreasing segment
        
        lower_idx = np.argmin(segment)
        lower_time = time.iloc[start + lower_idx]
        
        trough_label = f'T{idx+1}'  # Trough label (e.g., T1, T2, T3, ...)
        
        plt.plot(lower_time, lower, "go", label="Lower Value" if idx == 0 else "")  # Mark lower value
        
        plt.text(lower_time, lower, f'{trough_label}\nTime: {lower_time}\nValue: {lower:.5f}', fontsize=9, ha='right', color='black')

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor} (Lower Peaks)")
    plt.legend()

    # Print the number of lower peaks
    print(f"Number of lower peaks for {sensor}: {len(lower_values)}")

plt.tight_layout()
plt.show()
