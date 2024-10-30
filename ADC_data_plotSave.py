import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import atexit
import keyboard  # Import the keyboard library for keyboard interrupt
import os
from datetime import datetime  # Import to get the current date and time

# Set up the serial port (adjust 'COMx' for Windows or '/dev/ttyUSBx' for Linux/Mac)
ser = serial.Serial('COM4', 115200, timeout=1)  # Adjust this for your setup
ser.flush()  # Clear old data from serial buffer

# Create a directory with the current date and time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Format date and time as YYYY-MM-DD_HH-MM-SS
if not os.path.exists(current_time):
    os.makedirs(current_time)  # Create directory if it doesn't exist

# Create a figure and axis for the plot
fig, ax = plt.subplots()
x_data, y_data = [], []  # Lists to store time and sensor values
line, = ax.plot([], [], lw=2, color='green')  # Initialize an empty plot line with green color

# Record the start time to calculate elapsed time for X-axis
start_time = time.perf_counter()  # More precise than time.time()

# Open a file to store the data in the date-time named folder
data_file_path = os.path.join(current_time, 'sensor_data.txt')  # File path for the data
data_file = open(data_file_path, 'w')  # Open a file for writing
data_file.write("Time (s), Sensor Value (ADC)\n")  # Write header to the file

# To store the complete dataset for final plotting
complete_x_data = []
complete_y_data = []

def cleanup():
    """Function to run on exit to save the final plot."""
    data_file.close()  # Close the data file
    print(f"Data saved to {data_file_path}")  # Confirmation message
    
    # Plot the entire dataset with Y values adjusted
    if complete_x_data and complete_y_data:
        plt.figure()  # Create a new figure for final plot
        plt.plot(complete_x_data, complete_y_data, lw=2, color='green')  # Plot in green
        plt.title("Complete Sensor Data")
        plt.xlabel("Time (s)")
        plt.ylabel("Sensor Data")

        # Show max and min values on the plot
        plt.annotate(f'Max: {max(complete_y_data):.2f}', xy=(complete_x_data[-1], max(complete_y_data)), 
                     xytext=(complete_x_data[-1], max(complete_y_data) + 50), 
                     arrowprops=dict(arrowstyle='->', color='red'), color='red')
        plt.annotate(f'Min: {min(complete_y_data):.2f}', xy=(complete_x_data[-1], min(complete_y_data)), 
                     xytext=(complete_x_data[-1], min(complete_y_data) - 50), 
                     arrowprops=dict(arrowstyle='->', color='green'), color='green')

        plt.xticks(range(0, int(max(complete_x_data)) + 10, 5))  # Set x-ticks at every 5 seconds
        plt.yticks(range(0, int(max(complete_y_data)) + 100, 100))  # Set y-ticks with difference of 100
        plt.grid()

        # Save the final plot as an image in the date-time named folder
        plot_file_path = os.path.join(current_time, 'final_sensor_data_plot.png')  # Path for plot image
        plt.savefig(plot_file_path)  # Save the final plot as an image
        print(f"Plot saved to {plot_file_path}")  # Confirmation message
        plt.show()  # Show the final plot

# Register the cleanup function to run on exit
atexit.register(cleanup)

def update(frame):
    """This function reads data from the serial port and updates the plot."""
    if ser.in_waiting > 0:  # Check if data is available in the buffer
        try:
            data = ser.readline().decode('utf-8').strip()  # Read and decode data
            raw_value = int(data.split()[2])  # Extract the sensor value

            # Calculate elapsed time in seconds
            elapsed_time = time.perf_counter() - start_time

            # Append new data to the lists
            x_data.append(elapsed_time)
            y_data.append(raw_value)

            # Store the complete dataset for final plotting
            complete_x_data.append(elapsed_time)
            complete_y_data.append(raw_value)

            # Write the new data to the file
            data_file.write(f"{elapsed_time:.2f}, {raw_value}\n")  # Write time and value to the file

            # Print for debugging
            print(f"Time: {elapsed_time:.2f} s, Sensor Value: {raw_value}")

            # Limit the plot to the last 100 data points for better readability
            if len(x_data) > 100:
                x_data.pop(0)
                y_data.pop(0)

            # Update the plot with new data
            line.set_data(x_data, y_data)  # Use original Y-values for real-time plot
            ax.relim()  # Recompute axis limits
            ax.autoscale_view(True, True, True)  # Autoscale the view

            # Set X and Y ticks
            ax.set_xticks(range(0, int(max(x_data)) + 10, 5))  # Set x-ticks at every 5 seconds
            ax.set_yticks(range(0, int(max(y_data)) + 100, 100))  # Set y-ticks with difference of 100
            ax.grid()

        except Exception as e:
            print(f"Error: {e}")  # Print any errors for debugging

    return line,

# Function to handle keyboard interrupt
def handle_keyboard_interrupt():
    print("Keyboard interrupt received. Exiting...")
    plt.close(fig)  # Close the plot to trigger cleanup

# Register keyboard interrupt handler
keyboard.add_hotkey('q', handle_keyboard_interrupt)  # Press 'q' to exit

# Set up the animation function to update the plot every 100ms
ani = FuncAnimation(fig, update, blit=True, interval=10)

# Plot labels and title
plt.title("Real-Time Sensor Data")
plt.xlabel("Time (s)")
plt.ylabel("Sensor Data")  # Change label to "Sensor Data"

# Show the plot
plt.show()
