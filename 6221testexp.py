from instruments.keithley_6221 import Keithley6221Instrument

# Initialize the instrument
try:
    keithley = Keithley6221Instrument()
except ValueError as e:
    print(e)
    exit()  # Stop if the instrument is not found

# Run a waveform generation test
result = keithley.generate_waveform(amplitude=0.02, frequency=1000, duty_cycle=50, duration_cycles=20)

# Print waveform details
print("Waveform Generation Results:")
for key, value in result.items():
    print(f"{key}: {value}")
