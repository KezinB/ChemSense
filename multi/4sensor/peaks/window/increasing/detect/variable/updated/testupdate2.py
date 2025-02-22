import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load data
file_path = r"C:\Users\kezin\OneDrive\Documents\Accubits\Programs\multi\4sensor\peaks\test_3_02_25.csv"
try:
    df = pd.read_csv(file_path, encoding="ISO-8859-1")
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding="latin1")

# Configuration
UPPER_WINDOW = 15  # Smaller window for sharp upper peaks
LOWER_WINDOW = 30  # Larger window for broader lower trends
MIN_PEAK_HEIGHT = 0.1  # Adjust based on your data scale

time = df["Time"]
valid_sensors = df.columns[7:9]  # Update based on your CSV structure

plt.figure(figsize=(15, 10))

for i, sensor in enumerate(valid_sensors):
    data = df[sensor].values
    plt.subplot(len(valid_sensors), 1, i+1)
    plt.plot(time, data, 'b-', label='Raw Data')
    
    # Smooth data for trend analysis
    smooth_data = pd.Series(data).rolling(window=UPPER_WINDOW, center=True).mean().values
    
    # Find upper peaks (mountain peaks) using smaller window
    upper_peaks, _ = find_peaks(smooth_data, height=MIN_PEAK_HEIGHT, distance=UPPER_WINDOW)
    upper_mins = []
    
    # Find valleys between upper peaks
    for j in range(len(upper_peaks)-1):
        segment = smooth_data[upper_peaks[j]:upper_peaks[j+1]]
        upper_mins.append(upper_peaks[j] + np.argmin(segment))
    
    # Find lower trends using larger window
    lower_peaks, _ = find_peaks(-smooth_data, distance=LOWER_WINDOW)  # Valleys become peaks when inverted
    lower_maxs = []
    
    # Process lower segments
    for j in range(len(lower_peaks)-1):
        segment = smooth_data[lower_peaks[j]:lower_peaks[j+1]]
        lower_maxs.append(lower_peaks[j] + np.argmax(segment))
    
    # Plot upper features
    plt.plot(time.iloc[upper_peaks], data[upper_peaks], 'ro', label='Upper Max')
    plt.plot(time.iloc[upper_mins], data[upper_mins], 'go', label='Upper Min')
    
    # Plot lower features
    plt.plot(time.iloc[lower_peaks], data[lower_peaks], 'mv', label='Lower Min')
    plt.plot(time.iloc[lower_maxs], data[lower_maxs], 'cx', label='Lower Max')
    
    # Number the mountains
    for idx, (peak, valley) in enumerate(zip(upper_peaks, upper_mins)):
        plt.text(time.iloc[peak], data[peak], f'M{idx+1}\n({data[peak]:.2f})', 
                 ha='center', va='bottom', color='red')
        plt.text(time.iloc[valley], data[valley], f'v{idx+1}\n({data[valley]:.2f})', 
                 ha='center', va='top', color='green')
    
    plt.title(f'Sensor {sensor} - Feature Detection')
    plt.legend()

plt.tight_layout()
plt.show()