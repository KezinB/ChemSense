import matplotlib.pyplot as plt

# Function to read data from a text file
def read_data(file_path):
    times = []
    values = []
    
    with open(file_path, 'r') as file:
        # Skip the header line if it exists
        header = file.readline()  # Read and ignore the first line
        
        for line in file:
            # Assuming the format is "time,value" or "time value"
            time, value = map(float, line.strip().split())
            times.append(time)
            values.append(value)
    
    return times, values

# Function to plot the data
def plot_data(times, values):
    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker='o')
    plt.title('Time vs Value')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid()
    plt.show()

# Main function
if __name__ == "__main__":
    file_path = r'C:\Users\HP\OneDrive\Documents\Accubits\Programs\sensor_data.txt'  # Replace with your file path
    times, values = read_data(file_path)
    plot_data(times, values)
