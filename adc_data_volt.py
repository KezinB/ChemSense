import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import atexit
import keyboard  # For keyboard interrupt handling
import os
from datetime import datetime
import numpy as np  # Import numpy for creating float ranges

# Ask the user for sensor name and initial resistance
sensor_name = input("Enter the sensor name: ")
initial_resistance = input("Enter the initial resistance (in ohms): ")

# Set up the serial port (adjust 'COMx' for Windows or '/dev/ttyUSBx' for Linux/Mac)
ser = serial.Serial('COM5', 115200, timeout=1)  # Adjust for your setup
ser.flush()  # Clear old data from serial buffer

# Record the start time
start_time = time.perf_counter()  # Start timing from now
formatted_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Create a directory with the current date and time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if not os.path.exists(current_time):
    os.makedirs(current_time)  # Create directory if it doesn't exist

# Create a figure and axis for the plot
fig, ax = plt.subplots()
x_data, y_data = [], []  # Lists to store time and voltage values
line, = ax.plot([], [], lw=2, color='green', label='Voltage Data')  # Initialize an empty plot line with green color

# Open a file to store data with metadata
data_file_path = os.path.join(current_time, 'sensor_data.txt')
data_file = open(data_file_path, 'w')

# Write the sensor name and initial resistance as metadata
data_file.write(f"Sensor Name: {sensor_name}\n")
data_file.write(f"Initial Resistance: {initial_resistance} ohms\n")
data_file.write(f"Start Time: {formatted_start_time}\n")
data_file.write("Time (s), Voltage (V)\n")

# Complete dataset for final plotting
complete_x_data = []
complete_y_data = []

def cleanup():
    """Function to run on exit to save the final plot."""
    data_file.close()
    print(f"Data saved to {data_file_path}")

    # Record the end time
    end_time = datetime.now()
    formatted_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Plot the entire dataset with Y values adjusted
    if complete_x_data and complete_y_data:
        plt.figure()
        plt.plot(complete_x_data, complete_y_data, lw=2, color='green', label='Voltage Data')
        plt.title(f"Complete Sensor Data\nSensor: {sensor_name}, Initial Resistance: {initial_resistance} ohms")
        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (V)")

        # Show max and min values on the plot
        max_value = max(complete_y_data)
        min_value = min(complete_y_data)
        plt.axhline(y=max_value, color='red', linestyle='--', label=f'Max: {max_value:.4f} V')
        plt.axhline(y=min_value, color='blue', linestyle='--', label=f'Min: {min_value:.4f} V')

        plt.annotate(f'Max: {max_value:.4f}', xy=(complete_x_data[-1], max_value), 
                     xytext=(complete_x_data[-1], max_value + 0.5), 
                     arrowprops=dict(arrowstyle='->', color='red'), color='red')
        plt.annotate(f'Min: {min_value:.4f}', xy=(complete_x_data[-1], min_value), 
                     xytext=(complete_x_data[-1], min_value - 0.5), 
                     arrowprops=dict(arrowstyle='->', color='blue'), color='blue')

        # Set limits for x and y axes
        plt.xlim(0, max(complete_x_data) + 5)  # Add some buffer to the right of the last time point
        plt.ylim(0, 5)  # Y-axis limit set to 5V

        # Set X and Y ticks
        ax.set_xticks(range(0, int(max(complete_x_data)) + 10, 10))  # X-ticks every 10 seconds
        ax.set_yticks(np.arange(0, 5.2, 0.2))  # Y-ticks with voltage range 0 to 5V in 0.2V intervals
        plt.grid()

        # Annotate start and end times on the plot
        plt.annotate(f'Start Time: {formatted_start_time}', xy=(0.05, 0.95), xycoords='axes fraction',
                     fontsize=10, color='blue', weight='bold')
        plt.annotate(f'End Time: {formatted_end_time}', xy=(0.05, 0.90), xycoords='axes fraction',
                     fontsize=10, color='blue', weight='bold')

        # Add legend
        plt.legend()

        # Save the final plot in the date-time named folder
        plot_file_path = os.path.join(current_time, 'final_sensor_data_plot.png')
        plt.savefig(plot_file_path)
        print(f"Plot saved to {plot_file_path}")
        plt.show()

# Register cleanup function to run on exit
atexit.register(cleanup)

def update(frame):
    """This function reads data from the serial port and updates the plot."""
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip()
            raw_value = int(data.split()[2])  # Extract the sensor value

            # Map raw ADC value to voltage (assuming 10-bit ADC, range 0-1023)
            voltage = raw_value * (5.0 / 1023.0)

            # Calculate elapsed time in seconds from the start of the program
            elapsed_time = time.perf_counter() - start_time

            # Append new data to lists
            x_data.append(elapsed_time)
            y_data.append(voltage)

            # Store complete dataset for final plotting
            complete_x_data.append(elapsed_time)
            complete_y_data.append(voltage)

            # Write the new data to file with voltage formatted to 4 decimal places
            data_file.write(f"{elapsed_time:.2f}, {voltage:.4f}\n")

            print(f"Time: {elapsed_time:.2f} s, Voltage: {voltage:.4f} V")

            # Limit to last 100 data points for real-time plot readability
            if len(x_data) > 100:
                x_data.pop(0)
                y_data.pop(0)

            # Update plot with new data
            line.set_data(x_data, y_data)
            ax.relim()
            ax.autoscale_view(True, True, True)

            # Set X and Y ticks
            ax.set_xticks(range(0, int(max(x_data)) + 10, 10))  # X-ticks every 10 seconds
            ax.set_yticks(np.arange(0, 5.2, 0.2))  # Y-ticks with voltage range 0 to 5V in 0.2V intervals
            ax.grid()

        except Exception as e:
            print(f"Error: {e}")

    return line,

# Function to handle keyboard interrupt
def handle_keyboard_interrupt():
    print("Keyboard interrupt received. Exiting...")
    plt.close(fig)  # Close plot to trigger cleanup

# Register keyboard interrupt handler
keyboard.add_hotkey('q', handle_keyboard_interrupt)  # Press 'q' to exit

# Set up the animation function
ani = FuncAnimation(fig, update, blit=True, interval=1)  # Update every 100ms

# Plot labels and title
plt.title(f"Real-Time Voltage Data\nSensor: {sensor_name}, Initial Resistance: {initial_resistance} ohms")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")

# Show the plot
plt.show()
