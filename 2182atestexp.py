# from instruments.keithley_2182a import Keithley2182Instrument


# keithley = Keithley2182Instrument()
# avgVolts, stdVolts, samples = keithley.measure_nanovoltage(samples=100, nplc=5)

# print ("Voltage: ", avgVolts["Average Voltage"])




import numpy as np
import matplotlib.pyplot as plt
from instruments.keithley_2182a import Keithley2182Instrument

# Initialize the instrument
try:
    keithley = Keithley2182Instrument()
except ValueError as e:
    print(e)
    exit()  # Stop if the instrument is not found

# Run a test voltage measurement
result = keithley.measure_nanovoltage(samples=50, nplc=5)

# Print results
print(f"Average Voltage: {result['Average Voltage']} V")
print(f"Standard Deviation: {result['Standard Deviation']} V")
