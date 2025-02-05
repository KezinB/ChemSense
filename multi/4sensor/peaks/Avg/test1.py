import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

    # Calculate rolling average
    # rolling_avg = data.rolling(window=5).mean()
    rolling_avg = data.rolling(window=10).mean()

    # Detect points with sudden increase and then sudden decrease
    trend_points = []
    for j in range(1, len(rolling_avg) - 1):
        if rolling_avg[j] > rolling_avg[j - 1] and rolling_avg[j] > rolling_avg[j + 1]:
            if data[j] - data[j - 1] > np.std(data) and data[j] - data[j + 1] > np.std(data):
                trend_points.append(j)

    # Plot original data and rolling average
    plt.subplot(len(valid_sensors), 1, i + 1)
    plt.plot(time, data, label=sensor, color='blue')
    plt.plot(time, rolling_avg, label="Rolling Average", color='green')
    plt.plot(time.iloc[trend_points], data.iloc[trend_points], "ro", label="Trend Points")  # Mark trend points
    
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Sensor: {sensor}")
    plt.legend()

plt.tight_layout()
plt.show()
