import serial
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize serial connection
# ser = serial.Serial('COM9', baudrate=115200, timeout=10)  # Replace 'COM9' with your actual COM port
ser = serial.Serial('COM4', baudrate=9600, timeout=10)  
# Create a filename with the current date and time
filename = "C:\\Users\\user\\OneDrive\\Documents\\Accubits\\Programs\\multi\\2sensor\\test3-comb_voltage_log_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
with open(filename, "w") as file:
    file.write("Time, Voltage1, Voltage2\n")

# Lists to store the data
data_A0 = []
data_A1 = []

# Create a function to update the plot
def update(frame):
    line = ser.readline().decode("utf-8").strip()
    print(line)
    if line:
        try:
            values = list(map(float, line.split(',')))
            if len(values) > 0:
                data_A0.append(values[0])
                if len(values) > 1:
                    data_A1.append(values[1])
                
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                with open(filename, "a") as file:
                    file.write("{}, {}, {}\n".format(current_time, values[0], values[1] if len(values) > 1 else ''))
                
                # ax1.cla()
                # if len(data_A1) > 0:
                #     ax2.cla()
                ax3.cla()
                
                # ax1.plot(data_A0, color='blue', label='Sensor 1')
                # ax1.set_title('Live Voltage Plot Sensor 1')
                # ax1.set_xlabel('Time')
                # ax1.set_ylabel('Voltage')
                # ax1.relim()
                # ax1.autoscale_view()
                # ax1.legend(loc='upper right')
                
                # if len(data_A1) > 0:
                #     ax2.plot(data_A1, color='red', label='Sensor 2')
                #     ax2.set_title('Live Voltage Plot Sensor 2')
                #     ax2.set_xlabel('Time')
                #     ax2.set_ylabel('Voltage')
                #     ax2.relim()
                #     ax2.autoscale_view()
                #     ax2.legend(loc='upper right')
                
                ax3.plot(data_A0, color='blue', label='Sensor 1')
                if len(data_A1) > 0:
                    ax3.plot(data_A1, color='red', label='Sensor 2')
                ax3.set_title('Combined Live Voltage Plot')
                ax3.set_xlabel('Time')
                ax3.set_ylabel('Voltage')
                ax3.relim()
                ax3.autoscale_view()
                ax3.legend(loc='upper right')

        except ValueError:
            # Handle the case where the data is not a valid float
            pass
    
    return line,

# Create a figure and axis for the plot
# fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
fig, ax3 = plt.subplots()
x, y = [], []

# Set titles and labels for axes
# ax1.set_title('Live Voltage Plot Sensor 1')
# ax1.set_xlabel('Time')
# ax1.set_ylabel('Voltage')
# ax1.legend()

# ax2.set_title('Live Voltage Plot Sensor 2')
# ax2.set_xlabel('Time')
# ax2.set_ylabel('Voltage')
# ax2.legend()

ax3.set_title('Combined Live Voltage Plot')
ax3.set_xlabel('Time')
ax3.set_ylabel('Voltage')
ax3.legend()

# Create an animation to update the plot
ani = animation.FuncAnimation(fig, update, interval=30)  # Adjust the interval based on your data rate (in milliseconds)

# Show the plot
plt.tight_layout()
plt.show()
