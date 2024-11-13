import serial
import datetime

ser = serial.Serial('COM5', baudrate=115200, timeout=10)

filename = "Voltage_log_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
with open(filename, "w") as file:
    file.write("Time, Voltage\n")    
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    while datetime.datetime.now() < end_time:
        ser.write(b"CONF:VOLT:DC 5.0\r\n")
        ser.write(b"MEAS:VOLT:DCAC?\r\n")
        ser.write(b"CONF:VOLT:DC 5.0\r\n")
        
        data = ser.readline().decode("utf-8").strip()
        if (data!=None):
            print(data)
            # extract the resistance value and current time
            resistance = str(data)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            # write the data to the file
            file.write("{}, {}\n".format(current_time, resistance))

ser.close()