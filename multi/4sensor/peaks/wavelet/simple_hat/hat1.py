import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pywt
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
    data = df[sensor].fillna(method="ffill")  # Handle missing values

    # **Wavelet Transform**
    wavelet = "mexh"  # Mexican Hat wavelet (good for peak detection)
    scales = np.arange(1, 50)  # Different scales for wavelet transform
    coefficients, _ = pywt.cwt(data, scales, wavelet)  

    # Get the most significant wavelet scale
    cwt_signal = coefficients[10]  # Scale 10 (adjustable for sensitivity)

    # **Detect Peaks Using CWT**
    peaks, _ = find_peaks(cwt_signal, height=np.mean(cwt_signal) + np.std(cwt_signal))
    
    # **Detect Decrease and Stabilization Points**
    decreases = []
    stabilizations = []
    
    for peak_idx in peaks:
        # Find first decreasing point after peak
        for j in range(peak_idx, len(data) - 1):
            if cwt_signal[j] > cwt_signal[j + 1]:  # Signal starts decreasing
                decreases.append(j)
                break
        
        # Find first stabilization point after decrease
        for j in range(decreases[-1], len(data) - 10):  # Scan ahead
            window = cwt_signal[j:j + 10]
            if np.max(window) - np.min(window) < 0.0005:  # Small variation = stabilized
                stabilizations.append(j)
                break

    # Store detected points
    key_points[sensor] = {
        "Peaks": [(time.iloc[p], data.iloc[p]) for p in peaks],
        "Decrease": [(time.iloc[d], data.iloc[d]) for d in decreases],
        "Stabilization": [(time.iloc[s], data.iloc[s]) for s in stabilizations],
    }

    # **Plot Results**
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')

    # Mark detected points
    for t, v in key_points[sensor]["Peaks"]:
        plt.scatter(t, v, color='red', label="Peak" if i == 0 else "", s=80)
    for t, v in key_points[sensor]["Decrease"]:
        plt.scatter(t, v, color='green', label="Decrease" if i == 0 else "", s=80)
    for t, v in key_points[sensor]["Stabilization"]:
        plt.scatter(t, v, color='purple', label="Stabilization" if i == 0 else "", s=80)

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
