from instruments.keithley_2450 import Keithley2450Instrument


keithley = Keithley2450Instrument()
voltages, currents = keithley.iv_measurement(current_min=1e-3, current_max=1e-3,data_points=10, measurements=10)

print ("voltage", voltages)
