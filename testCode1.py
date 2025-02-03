import serial
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates

# Initialize serial connection
ser = serial.Serial('COM4', baudrate=9600, timeout=10)

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
            current_time = datetime.datetime.now()
            x.append(current_time)
            y.append(data)
            line.set_data(x, y)
            ax.relim()
            ax.autoscale_view()
        except ValueError:
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

# Format the x-axis for dates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
fig.autofmt_xdate()

# Create an animation to update the plot
ani = animation.FuncAnimation(fig, update, interval=10)  # 100ms interval for smooth updates

# Show the plot
plt.show()
