import serial
import time
import matplotlib.pyplot as plt

# Set up the serial connection (adjust the port and baud rate as needed)
ser = serial.Serial('COM3', 115200, timeout=1)

# Lists to store the time and voltage values
time_list = []
volts_list = []

# Set the start time
start_time = time.time()

try:
    while True:
        # Read a line of data from the serial port
        line = ser.readline().decode('utf-8').strip()

        if line:
            # Check if the line contains a valid float
            try:
                volts0 = float(line)
                
                # Append the time and voltage to the lists
                time_list.append(time.time() - start_time)
                volts_list.append(volts0)

                # Print the voltage for debugging
                print("AIN0: {:.6f} V".format(volts0))

                # Plot the data
                plt.clf()
                plt.plot(time_list, volts_list, label='AIN0')
                plt.xlabel('Time (s)')
                plt.ylabel('Voltage (V)')
                plt.title('Voltage over Time')
                plt.legend()
                plt.pause(0.001)
                #plt.show()

            except ValueError:
                print(f"Invalid data: {line}")

        # Delay for a bit to simulate real-time plotting
        time.sleep(1)

except KeyboardInterrupt:
    print("Plotting stopped.")
    ser.close()

# Show the final plot
plt.show()
