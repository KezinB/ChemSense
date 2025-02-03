import serial
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize serial connection
ser = serial.Serial('COM4', baudrate=115200, timeout=10)  # Replace 'COM4' with your actual COM port

# Create a filename with the current date and time
filename = "C:\\Users\\user\\OneDrive\\Documents\\Accubits\\Programs\\multi\\4sensor\\test4-comb_voltage_log_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
with open(filename, "w") as file:
    file.write("Time, Voltage1, Voltage2, Voltage3, Voltage4\n")

# Lists to store the data
data_A0 = []
data_A1 = []
data_A2 = []
data_A3 = []

# Create a function to update the plot
def update(frame):
    line = ser.readline().decode("utf-8").strip()
    print(line)
    if line:
        try:
            values = list(map(float, line.split('|')))
            if len(values) >= 4:
                data_A0.append(values[0])
                data_A1.append(values[1])
                data_A2.append(values[2])
                data_A3.append(values[3])
                
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                with open(filename, "a") as file:
                    file.write("{}, {}, {}, {}, {}\n".format(current_time, values[0], values[1], values[2], values[3]))
                
                ax.cla()
                ax.plot(data_A0, color='blue', label='Sensor 1')
                ax.plot(data_A1, color='red', label='Sensor 2')
                ax.plot(data_A2, color='green', label='Sensor 3')
                ax.plot(data_A3, color='orange', label='Sensor 4')
                ax.set_title('Combined Live Voltage Plot')
                ax.set_xlabel('Time')
                ax.set_ylabel('Voltage')
                ax.relim()
                ax.autoscale_view()
                ax.legend(loc='upper right')

        except ValueError:
            # Handle the case where the data is not a valid float
            pass
    
    return line,

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Set titles and labels for axes
ax.set_title('Combined Live Voltage Plot')
ax.set_xlabel('Time')
ax.set_ylabel('Voltage')
ax.legend()

# Create an animation to update the plot
ani = animation.FuncAnimation(fig, update, interval=50)  # Adjust the interval based on your data rate (in milliseconds)

# Show the plot
plt.tight_layout()
plt.show()
