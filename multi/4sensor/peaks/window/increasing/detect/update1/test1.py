import pandas as pd
import numpy as np

# Load the CSV file
file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_final.csv"  # Update with your file path
df = pd.read_csv(file_path, encoding="ISO-8859-1")

# Extract relevant sensor columns and time
time = df["Time"]
sensor_4 = df["Sensor 4 (V)"]
sensor_5 = df["Sensor 5 (V)"]

# Function to detect key points
def detect_key_points(time, signal):
    # Find the peak (highest value)
    peak_idx = np.argmax(signal)
    
    # Find start point (first non-NaN value)
    start_idx = signal.first_valid_index()
    
    # Find decrease point (first significant drop after peak)
    decrease_idx = peak_idx + np.where(np.diff(signal[peak_idx:].values) < 0)[0][0] + 1
    
    # Find stabilization point (where it flattens out)
    diff_signal = np.abs(np.diff(signal))
    stability_idx = decrease_idx + np.where(diff_signal[decrease_idx:] < np.mean(diff_signal) * 0.1)[0][0] + 1

    return {
        "Start": (time[start_idx], signal[start_idx]),
        "Peak": (time[peak_idx], signal[peak_idx]),
        "Decrease": (time[decrease_idx], signal[decrease_idx]),
        "Stabilization": (time[stability_idx], signal[stability_idx]),
    }

# Detect key points for both sensors
key_points_4 = detect_key_points(time, sensor_4)
key_points_5 = detect_key_points(time, sensor_5)

# Print results
print("Sensor 4 Key Points:", key_points_4)
print("Sensor 5 Key Points:", key_points_5)
