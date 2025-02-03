import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up the serial port connection
ser = serial.Serial('COM9', baudrate=115200, timeout=10)  # Replace 'COM9' with your actual COM port

# Lists to store the data
data_A0 = []
data_A1 = []

def update(frame):
    line = ser.readline().decode('utf-8').strip()
    print(line)
    if line:
        try:
            values = list(map(float, line.split(',')))
            if len(values) > 0:
                data_A0.append(values[0])
                # data_A1.append(values[1])
                
                ax1.cla()
                # ax2.cla()
                # ax3.cla()
                
                ax1.plot(data_A0, color='blue', label='Sensor 1')
                ax1.set_title('Live Voltage Plot Sensor 1')
                ax1.set_xlabel('Time')
                ax1.set_ylabel('Voltage')
                ax1.relim()
                ax1.autoscale_view()
                ax1.legend(loc='upper right')
                
                # ax2.plot(data_A1, color='red', label='Sensor 2')
                # ax2.set_title('Live Voltage Plot Sensor 2')
                # ax2.set_xlabel('Time')
                # ax2.set_ylabel('Voltage')
                # ax2.relim()
                # ax2.autoscale_view()
                # ax2.legend(loc='upper right')
                
                # ax3.plot(data_A0, color='blue', label='Sensor 1')
                # ax3.plot(data_A1, color='red', label='Sensor 2')
                # ax3.set_title('Combined Live Voltage Plot')
                # ax3.set_xlabel('Time')
                # ax3.set_ylabel('Voltage')
                # ax3.relim()
                # ax3.autoscale_view()
                # ax3.legend(loc='upper right')
        except ValueError:
            pass

# fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig, ax1 = plt.subplots()

ani = FuncAnimation(fig, update, interval=30)

plt.tight_layout()
plt.show()
