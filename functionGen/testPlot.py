import serial
import matplotlib.pyplot as plt
import time

# Initialize serial connection
ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to be established

data = []  # List to store data from serial port

try:
    while True:
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
        if line:
            print(line)  # Print the data to the console for debugging
            data.append(float(line))  # Convert the line to a float and add to the list

            # Plot the data
            plt.clf()  # Clear the current figure
            plt.plot(data)  # Plot the data
            plt.xlabel('Time')
            plt.ylabel('Value')
            plt.title('Serial Data from COM3')
            plt.pause(0.1)  # Pause to update the plot

except KeyboardInterrupt:
    # Stop the loop if Ctrl+C is pressed
    pass

# Close the serial connection
ser.close()

# Show the final plot
plt.show()
