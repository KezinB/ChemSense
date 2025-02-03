import serial
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize serial connection
ser = serial.Serial('COM9', baudrate=115200, timeout=10)

# Create a filename with the current date and time
filename = "voltage_log_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
with open(filename, "w") as file:
    file.write("Time, Voltage\n")

end_time = datetime.datetime.now() + datetime.timedelta(minutes=600)

# Create a function to update the plot
def update(frame):
    ser.write(b"CONF:VOLT:DC \r\n")
    ser.write(b"MEAS:VOLT:DCAC?\r\n")
    ser.write(b"CONF:VOLT:DC \r\n")
    
    data = ser.readline().decode("utf-8").strip()
    print(data)
    if data:
        try:
            data = float(data)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            with open(filename, "a") as file:
                file.write("{}, {}\n".format(current_time, data))
            
            x.append(frame)
            y.append(data)
            line.set_data(x, y)
            ax.relim()
            ax.autoscale_view()
        except ValueError:
            # Handle the case where the data is not a valid float
            pass
    
    return line,

# Create a figure and axis for the plot
fig, ax = plt.subplots()
x, y = [], []
line, = ax.plot([], [], label='Serial Data')
ax.set_title('Live Voltage Plot')
ax.set_xlabel('Time')
ax.set_ylabel('Voltage')
ax.legend()

# Create an animation to update the plot
ani = animation.FuncAnimation(fig, update, interval=30 )  # Adjust the interval based on your data rate (in milliseconds)

# Show the plot
plt.show()
   