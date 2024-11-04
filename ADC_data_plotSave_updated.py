import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import atexit
import keyboard  # For keyboard interrupt handling
import os
from datetime import datetime

# Ask the user for sensor name and initial resistance
sensor_name = input("Enter the sensor name: ")
initial_resistance = input("Enter the initial resistance (in ohms): ")

# Set up the serial port (adjust 'COMx' for Windows or '/dev/ttyUSBx' for Linux/Mac)
ser = serial.Serial('COM4', 115200, timeout=1)  # Adjust for your setup
ser.flush()  # Clear old data from serial buffer

# Create a directory with the current date and time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if not os.path.exists(current_time):
    os.makedirs(current_time)  # Create directory if it doesn't exist

# Create a figure and axis for the plot
fig, ax = plt.subplots()
x_data, y_data = [], []  # Lists to store time and sensor values
line, = ax.plot([], [], lw=2, color='green')  # Initialize an empty plot line with green color

# Record the start time to calculate elapsed time for X-axis
start_time = time.perf_counter()

# Open a file to store data with metadata
data_file_path = os.path.join(current_time, 'sensor_data.txt')
data_file = open(data_file_path, 'w')

# Write the sensor name and initial resistance as metadata
data_file.write(f"Sensor Name: {sensor_name}\n")
data_file.write(f"Initial Resistance: {initial_resistance} ohms\n")
data_file.write("Time (s), Sensor Value (ADC)\n")

# Complete dataset for final plotting
complete_x_data = []
complete_y_data = []

def cleanup():
    """Function to run on exit to save the final plot."""
    data_file.close()
    print(f"Data saved to {data_file_path}")
    
    # Plot the entire dataset with Y values adjusted
    if complete_x_data and complete_y_data:
        plt.figure()
        plt.plot(complete_x_data, complete_y_data, lw=2, color='green')
        plt.title(f"Complete Sensor Data\nSensor: {sensor_name}, Initial Resistance: {initial_resistance} ohms")
        plt.xlabel("Time (s)")
        plt.ylabel("Sensor Data")

        # Show max and min values on the plot
        plt.annotate(f'Max: {max(complete_y_data):.2f}', xy=(complete_x_data[-1], max(complete_y_data)), 
                     xytext=(complete_x_data[-1], max(complete_y_data) + 50), 
                     arrowprops=dict(arrowstyle='->', color='red'), color='red')
        plt.annotate(f'Min: {min(complete_y_data):.2f}', xy=(complete_x_data[-1], min(complete_y_data)), 
                     xytext=(complete_x_data[-1], min(complete_y_data) - 50), 
                     arrowprops=dict(arrowstyle='->', color='green'), color='green')

        plt.xticks(range(0, int(max(complete_x_data)) + 10, 5))  # X-ticks every 5 seconds
        plt.yticks(range(0, int(max(complete_y_data)) + 100, 100))  # Y-ticks with difference of 100
        plt.grid()

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

            # Calculate elapsed time in seconds
            elapsed_time = time.perf_counter() - start_time

            # Append new data to lists
            x_data.append(elapsed_time)
            y_data.append(raw_value)

            # Store complete dataset for final plotting
            complete_x_data.append(elapsed_time)
            complete_y_data.append(raw_value)

            # Write the new data to file
            data_file.write(f"{elapsed_time:.2f}, {raw_value}\n")

            print(f"Time: {elapsed_time:.2f} s, Sensor Value: {raw_value}")

            # Limit to last 100 data points for real-time plot readability
            if len(x_data) > 100:
                x_data.pop(0)
                y_data.pop(0)

            # Update plot with new data
            line.set_data(x_data, y_data)
            ax.relim()
            ax.autoscale_view(True, True, True)

            # Set X and Y ticks
            ax.set_xticks(range(0, int(max(x_data)) + 10, 5))  # X-ticks every 5 seconds
            ax.set_yticks(range(0, int(max(y_data)) + 100, 100))  # Y-ticks with difference of 100
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
ani = FuncAnimation(fig, update, blit=True, interval=10)

# Plot labels and title
plt.title(f"Real-Time Sensor Data\nSensor: {sensor_name}, Initial Resistance: {initial_resistance} ohms")
plt.xlabel("Time (s)")
plt.ylabel("Sensor Data")

# Show the plot
plt.show()
