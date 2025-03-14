import serial
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ser = serial.Serial('COM3', 9600) 
ser = serial.Serial('COM5', baudrate=115200, timeout=10)

filename = "resistance_log_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
with open(filename, "w") as file:
    file.write("Time, Resistance\n")

    ser.write(b"SAMP:COUN 1\r\n")    
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=360)


# Create a function to read data from the serial port
def get_serial_data():
    ser.write(b"SAMP:COUN 1\r\n")  
    ser.write(b"MEASure:RESistance?\r\n")
    data = ser.readline().decode("utf-8").strip()
    print(data)
    resistance = str(data)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    if data:
        with open(filename, "a") as file:
            file.write("{}, {}\n".format(current_time, resistance))
            return data
        
# Create a function to update the plot
def update(frame):
    while datetime.datetime.now() < end_time:
        data = float(get_serial_data())
        x.append(frame)
        y.append(data)
        line.set_data(x, y)
        ax.relim()
        ax.autoscale_view()
        return line,
    

# Create a figure and axis for the plot
fig, ax = plt.subplots()
x, y = [], []
line, = ax.plot([], [], label='Serial Data')
ax.set_title('Live Resistance Plot')
ax.set_xlabel('Time')
ax.set_ylabel('Resistance')
ax.legend()

# Create an animation to update the plot
ani = animation.FuncAnimation(fig, update, interval=100)  # Adjust the interval based on your data rate (in milliseconds)

# Show the plot
plt.show()

