import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Set up the serial port (adjust 'COMx' for Windows or '/dev/ttyUSBx' for Linux/Mac)
ser = serial.Serial('COM4', 115200, timeout=1)  # Adjust this for your setup
ser.flush()  # Clear old data from the serial buffer

# Create a figure and axis for the plot
fig, ax = plt.subplots()
x_data, y_data = [], []  # Lists to store time and sensor values
line, = ax.plot([], [], lw=2)  # Initialize an empty plot line

# Record the start time for calculating elapsed time
start_time = time.perf_counter()

# Open a text file in append mode to store the data
with open("sensor_data.txt", "a") as file:
    file.write("Time(s)\tSensor Value(ADC)\n")  # Write the header

    def update(frame):
        """Read data from the serial port and update the plot."""
        if ser.in_waiting > 0:  # Check if data is available
            try:
                data = ser.readline().decode('utf-8').strip()  # Read and decode data
                raw_value = int(data.split()[2])  # Extract the sensor value

                # Calculate elapsed time in seconds
                elapsed_time = time.perf_counter() - start_time

                # Append new data to the lists
                x_data.append(elapsed_time)
                y_data.append(raw_value)

                # Print for debugging
                print(f"Time: {elapsed_time:.2f} s, Sensor Value: {raw_value}")

                # Write data to the text file
                file.write(f"{elapsed_time:.2f}\t{raw_value}\n")
                file.flush()  # Ensure data is written to disk immediately

                # Limit the plot to the last 100 data points
                if len(x_data) > 100:
                    x_data.pop(0)
                    y_data.pop(0)

                # Update the plot
                line.set_data(x_data, y_data)
                ax.relim()  # Recompute limits
                ax.autoscale_view(True, True, True)  # Autoscale view
            except Exception as e:
                print(f"Error: {e}")  # Print any parsing errors

        return line,

    # Set up the animation function to update every 100 ms
    ani = FuncAnimation(fig, update, blit=True, interval=100)

    # Plot labels and title
    plt.title("Real-Time Sensor Data")
    plt.xlabel("Time (s)")
    plt.ylabel("Sensor Value (ADC)")
    plt.show()
