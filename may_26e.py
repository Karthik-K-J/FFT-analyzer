import serial
import numpy as np
import matplotlib.pyplot as plt

# Configure the serial port
port = 'COM3'  # Replace with the appropriate port for your Arduino
baud_rate = 9600
ser = serial.Serial(port, baud_rate)

# Number of data points to display in the time and frequency domain plots
num_samples = 2000

# Set the sampling rate
sampling_rate = 60

# Initialize lists to store data
timestamps = []
sensor_values = []

# Create empty plots
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
line1, = ax1.plot(timestamps, sensor_values, 'b-')
line2, = ax2.plot([], [], 'r-')
ax1.set_xlabel('Time')
ax1.set_ylabel('Amplitude')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Magnitude')
ax1.set_title('Real-time Time and Frequency Domain Plot')
ax1.grid(True)
ax2.grid(True)


# Frequency axis
freq = np.fft.rfftfreq(num_samples, d=1.0 / sampling_rate)

# Read and plot data
try:
    while True:
        # Read a line of data from the serial port
        line_data = ser.readline().decode().strip()

        # Split the line into timestamp and sensor value
        parts = line_data.split(',')
        timestamp = int(parts[0])
        sensor_value = float(parts[1])

        # Append data to lists
        timestamps.append(timestamp)
        sensor_values.append(sensor_value)

        # Limit the number of data points to display
        if len(timestamps) > num_samples:
            timestamps.pop(0)
            sensor_values.pop(0)

        # Update the time domain plot
        line1.set_data(timestamps, sensor_values)
        ax1.relim()
        ax1.autoscale_view(scalex=True, scaley=True)

        # Perform frequency analysis on a window of sensor values
        fft_values = np.zeros(num_samples)
        fft_values[:len(sensor_values)] = sensor_values - np.mean(sensor_values)  # Remove DC component

        # Update the frequency domain plot
        spectrum = np.abs(np.fft.rfft(fft_values))
        line2.set_data(freq, spectrum)
        ax2.relim()
        ax2.autoscale_view(scalex=True, scaley=True)

        # Redraw the plots
        fig.canvas.draw()
        plt.pause(0.01)

except KeyboardInterrupt:
    # Close the serial port on Ctrl+C
    ser.close()
