import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load the CSV file
file_path = file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_3_02_25.csv" # Update with your file path
df = pd.read_csv(file_path, encoding="ISO-8859-1")

# Extract relevant sensor columns and time
time = df["Time"]
sensor_4 = df["Sensor 4 (V)"]
sensor_5 = df["Sensor 5 (V)"]

# Function to detect multiple peaks and key points
def detect_multiple_peaks(time, signal):
    peaks, _ = find_peaks(signal, prominence=0.0009)  # Adjust prominence as needed
    start_idx = signal.first_valid_index()

    key_points = {"Start": (time[start_idx], signal[start_idx]), "Peaks": [], "Decrease": [], "Stabilization": []}

    for peak_idx in peaks:
        # Find decrease point after peak
        if peak_idx < len(signal) - 1:
            decrease_idx = peak_idx + np.where(np.diff(signal[peak_idx:].values) < 0)[0][0] + 1
        else:
            decrease_idx = peak_idx

        # Find stabilization point
        diff_signal = np.abs(np.diff(signal))
        stability_idx = decrease_idx + np.where(diff_signal[decrease_idx:] < np.mean(diff_signal) * 0.1)[0][0] + 1

        key_points["Peaks"].append((time[peak_idx], signal[peak_idx]))
        key_points["Decrease"].append((time[decrease_idx], signal[decrease_idx]))
        key_points["Stabilization"].append((time[stability_idx], signal[stability_idx]))

    return key_points

# Detect multiple key points for both sensors
key_points_4 = detect_multiple_peaks(time, sensor_4)
key_points_5 = detect_multiple_peaks(time, sensor_5)

# Function to plot sensor data with key points
def plot_sensor_data(time, signal, key_points, sensor_name):
    plt.figure(figsize=(10, 5))
    plt.plot(time, signal, label=f"{sensor_name} Data", color="blue")

    # Plot key points
    plt.scatter(*key_points["Start"], label="Start", marker="o", color="black", s=100)
    
    for t, v in key_points["Peaks"]:
        plt.scatter(t, v, label="Peak", marker="^", color="red", s=100)

    for t, v in key_points["Decrease"]:
        plt.scatter(t, v, label="Decrease", marker="v", color="green", s=100)

    for t, v in key_points["Stabilization"]:
        plt.scatter(t, v, label="Stabilization", marker="s", color="purple", s=100)

    plt.xlabel("Time")
    plt.ylabel("Sensor Voltage (V)")
    plt.title(f"{sensor_name} Sensor Data with Key Points")
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot Sensor 4
plot_sensor_data(time, sensor_4, key_points_4, "Sensor 4")

# Plot Sensor 5
plot_sensor_data(time, sensor_5, key_points_5, "Sensor 5")
