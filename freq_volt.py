import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import atexit
import keyboard  # For keyboard interrupt handling
import os
from datetime import datetime
import numpy as np
from scipy.signal import find_peaks  # Import find_peaks for peak detection

# Ask the user for sensor name and initial resistance
sensor_name = input("Enter the sensor name: ")
initial_resistance = input("Enter the initial resistance (in ohms): ")

# Set up the serial port (adjust 'COMx' for Windows or '/dev/ttyUSBx' for Linux/Mac)
ser = serial.Serial('COM4', 115200, timeout=1)  # Adjust for your setup
ser.flush()  # Clear old data from serial buffer

# Record the start time
start_time = time.perf_counter()
formatted_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Create a directory with the current date and time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if not os.path.exists(current_time):
    os.makedirs(current_time)  # Create directory if it doesn't exist

# Set up figure and axes for time-domain and frequency-domain plots
fig, (ax_time, ax_freq) = plt.subplots(2, 1, figsize=(10, 8))
x_data, y_data = [], []  # Time and voltage data for the time-domain plot
line_time, = ax_time.plot([], [], lw=2, color='green', label='Voltage Data')  # Time plot line

# Complete dataset for final plotting
complete_x_data = []
complete_y_data = []

# Frequency domain data
frequency_data = []
amplitude_data = []
line_freq, = ax_freq.plot([], [], lw=2, color='blue', label='Amplitude vs Frequency')  # Frequency plot line
peak_annotations = []  # To store peak annotations

# Open a file to store data with metadata
data_file_path = os.path.join(current_time, 'sensor_data.txt')
data_file = open(data_file_path, 'w')
data_file.write(f"Sensor Name: {sensor_name}\n")
data_file.write(f"Initial Resistance: {initial_resistance} ohms\n")
data_file.write(f"Start Time: {formatted_start_time}\n")
data_file.write("Time (s), Voltage (V)\n")

def cleanup():
    """Function to run on exit to save the final plot."""
    data_file.close()
    print(f"Data saved to {data_file_path}")
    
    # Save and show final time-domain plot
    if complete_x_data and complete_y_data:
        plt.figure()
        plt.plot(complete_x_data, complete_y_data, color='green')
        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (V)")
        plt.title("Complete Voltage Data")
        plt.savefig(os.path.join(current_time, 'final_time_domain_plot.png'))
        plt.show()
    
    # Save and show final frequency-domain plot
    if frequency_data and amplitude_data:
        plt.figure()
        plt.plot(frequency_data, amplitude_data, color='blue')
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.title("Frequency vs Amplitude")
        plt.savefig(os.path.join(current_time, 'final_frequency_domain_plot.png'))
        plt.show()

atexit.register(cleanup)

def update(frame):
    """This function reads data from the serial port and updates the plots."""
    global peak_annotations  # Modify the peak_annotations list
    
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip()
            raw_value = int(data.split()[2])  # Extract the sensor value
            voltage = raw_value * (5.0 / 1023.0)  # Convert ADC value to voltage
            
            # Calculate elapsed time in seconds
            elapsed_time = time.perf_counter() - start_time
            
            # Update time-domain data
            x_data.append(elapsed_time)
            y_data.append(voltage)
            complete_x_data.append(elapsed_time)
            complete_y_data.append(voltage)
            
            # Write the new data to file
            data_file.write(f"{elapsed_time:.2f}, {voltage:.4f}\n")
            
            # Limit to the last 10000 points for real-time plot readability
            if len(x_data) > 10000:
                x_data.pop(0)
                y_data.pop(0)
            
            # Update time-domain plot
            line_time.set_data(x_data, y_data)
            ax_time.relim()
            ax_time.autoscale_view(True, True, True)
            
            # Compute FFT and update frequency-domain plot
            if len(y_data) > 100:  # Ensure sufficient data points for FFT
                N = len(y_data)
                T = x_data[1] - x_data[0] if len(x_data) > 1 else 0.1  # Time step
                fft_result = np.fft.fft(y_data)
                fft_freqs = np.fft.fftfreq(N, T)[:N // 2]  # Only positive frequencies
                fft_amplitudes = 2.0 / N * np.abs(fft_result[:N // 2])  # Compute amplitude
                
                # Clear old data and add new frequency-domain data
                frequency_data.clear()
                amplitude_data.clear()
                frequency_data.extend(fft_freqs)
                amplitude_data.extend(fft_amplitudes)
                
                # Find peaks in the frequency spectrum
                peaks, _ = find_peaks(fft_amplitudes, height=0.1)  # Adjust height threshold as needed
                
                # Remove old peak annotations
                for annotation in peak_annotations:
                    annotation.remove()
                peak_annotations.clear()
                
                # Annotate peaks
                for peak in peaks:
                    freq = fft_freqs[peak]
                    amp = fft_amplitudes[peak]
                    annotation = ax_freq.annotate(f'{freq:.1f} Hz', xy=(freq, amp), 
                                                  xytext=(freq, amp + 0.1),
                                                  textcoords="offset points",
                                                  arrowprops=dict(arrowstyle="->", color='red'),
                                                  color='red', fontsize=8)
                    peak_annotations.append(annotation)
                
                # Update frequency-domain plot
                line_freq.set_data(frequency_data, amplitude_data)
                ax_freq.relim()
                ax_freq.autoscale_view(True, True, True)
                
        except Exception as e:
            print(f"Error: {e}")
    return line_time, line_freq

# Set up keyboard interrupt handler
def handle_keyboard_interrupt():
    print("Keyboard interrupt received. Exiting...")
    plt.close(fig)

keyboard.add_hotkey('q', handle_keyboard_interrupt)  # Press 'q' to exit

# Set up animation function
ani = FuncAnimation(fig, update, blit=True, interval=100)  # Update every 100ms

# Plot labels and titles
ax_time.set_title("Real-Time Voltage Data")
ax_time.set_xlabel("Time (s)")
ax_time.set_ylabel("Voltage (V)")
ax_time.grid()

ax_freq.set_title("Frequency vs Amplitude")
ax_freq.set_xlabel("Frequency (Hz)")
ax_freq.set_ylabel("Amplitude")
ax_freq.grid()

# Show the plots
plt.tight_layout()
plt.show()
