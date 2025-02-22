import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file
file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_3_02_25.csv"  # Update with your file path
df = pd.read_csv(file_path, encoding="ISO-8859-1")

# Extract relevant sensor columns and time
time = df["Time"]
sensor_4 = df["Sensor 4 (V)"]
sensor_5 = df["Sensor 5 (V)"]

# Function to detect key points
def detect_key_points(time, signal):
    peak_idx = np.argmax(signal)
    start_idx = signal.first_valid_index()
    decrease_idx = peak_idx + np.where(np.diff(signal[peak_idx:].values) < 0)[0][0] + 1
    diff_signal = np.abs(np.diff(signal))
    stability_idx = decrease_idx + np.where(diff_signal[decrease_idx:] < np.mean(diff_signal) * 0.1)[0][0] + 1

    return {
        "Start": (time[start_idx], signal[start_idx]),
        "Peak": (time[peak_idx], signal[peak_idx]),
        "Decrease": (time[decrease_idx], signal[decrease_idx]),
        "Stabilization": (time[stability_idx], signal[stability_idx]),
    }

# Detect key points
key_points_4 = detect_key_points(time, sensor_4)
key_points_5 = detect_key_points(time, sensor_5)

# Function to plot sensor data with key points
def plot_sensor_data(time, signal, key_points, sensor_name):
    plt.figure(figsize=(10, 5))
    plt.plot(time, signal, label=f"{sensor_name} Data", color="blue")

    # Plot key points
    for key, (t, v) in key_points.items():
        plt.scatter(t, v, label=key, marker="o", s=100)

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
