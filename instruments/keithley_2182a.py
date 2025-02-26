import numpy as np
import matplotlib.pyplot as plt
from pymeasure.instruments.keithley import Keithley2182

class Keithley2182Instrument:
    def __init__(self, address="GPIB0::7::INSTR"):
        self.nano = Keithley2182(address)
        self.nano.reset()
        self.nano.active_channel = 1
        self.nano.channel_function = "voltage"


    def measure_nanovoltage(self, samples=100, nplc=5):
        """
        Measures voltage using Keithley 2182A.
        """
        self.nano.ch_1.setup_voltage(auto_range=True, nplc=nplc)
        #==/Had to change self.nano.voltage to self.nano.voltage_nplc
        voltages = np.array([self.nano.voltage_nplc for _ in range(samples)])
        avg_voltage = np.mean(voltages)
        std_voltage = np.std(voltages)

        plt.plot(voltages, 'bo-')
        plt.xlabel("Sample Number")
        plt.ylabel("Voltage (V)")
        plt.title("Nanovoltmeter Readings")
        plt.grid(True)
        plt.show()

        return {"Average Voltage": avg_voltage, "Std Dev": std_voltage, "Samples": samples}
