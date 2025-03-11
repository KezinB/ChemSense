# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
# Load the CSV file (update the file path as needed)
# file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_3_02_25.csv"
# file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_final.csv"
file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\v4-plots\test5.csv"

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

# %%
# Create subplots for each sensor
plt.figure(figsize=(12, 12))

for i, sensor in enumerate(valid_sensors):
    data = df[sensor]
    
    increasing_segments = []
    segment_indices = []
    
    min_window_size = 15  # Minimum window size
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
    
    upper_values = [max(segment) for segment in increasing_segments]
    lower_values = [min(segment) for segment in increasing_segments]

    # Print detected values for the current sensor
    print(f"Sensor: {sensor}")
    for idx, (upper, lower) in enumerate(zip(upper_values, lower_values)):
        # Calculate R%
        R_percent = ((upper - lower) / lower) * 100
        
        print(f"Peak {idx + 1}:")
        print(f"  - Max Value: {upper:.5f}")
        print(f"  - Min Value: {lower:.5f}")
        print(f"  - R%: {R_percent:.2f}%")
    print("\n")  # Add a newline for better readability

    # Plot original data and mark upper and lower values of increasing segments
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    
    for idx, (indices, segment, upper, lower) in enumerate(zip(segment_indices, increasing_segments, upper_values, lower_values)):
        start, end = indices
        plt.plot(time.iloc[start:end], segment, "g", alpha=0.5)  # Highlight increasing segment
        
        upper_idx = np.argmax(segment)
        lower_idx = np.argmin(segment)
        
        upper_time = time.iloc[start + upper_idx]
        lower_time = time.iloc[start + lower_idx]
        
        peak_label = f'P{idx+1}'  # Peak label (e.g., P1, P2, P3, ...)
        
        plt.plot(upper_time, upper, "ro", label="Upper Value" if idx == 0 else "")  # Mark upper value
        plt.plot(lower_time, lower, "go", label="Lower Value" if idx == 0 else "")  # Mark lower value
        
        plt.text(upper_time, upper, f'{peak_label}\nTime: {upper_time}\nValue: {upper:.5f}', fontsize=9, ha='left', color='black')
        plt.text(lower_time, lower, f'Time: {lower_time}\nValue: {lower:.5f}', fontsize=9, ha='right', color='green')

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.grid(True)
    plt.legend()

plt.tight_layout()
plt.show()


