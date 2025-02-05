import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from sklearn.ensemble import IsolationForest

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
    data = df[sensor].values.reshape(-1, 1)

    # Initialize Isolation Forest
    iso_forest = IsolationForest(contamination=0.01, random_state=42)
    anomalies = iso_forest.fit_predict(data)

    # Indices of anomalies
    anomaly_indices = np.where(anomalies == -1)[0]

    # Plot original data
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, df[sensor], label=sensor, color='blue')
    plt.plot(time.iloc[anomaly_indices], df[sensor].iloc[anomaly_indices], "ro", label="Anomalies")  # Mark anomalies
    
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()
