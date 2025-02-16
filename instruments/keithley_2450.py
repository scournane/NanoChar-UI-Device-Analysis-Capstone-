import numpy as np
import matplotlib.pyplot as plt
from pymeasure.instruments.keithley import Keithley2450

class Keithley2450Instrument:
    def __init__(self, address="GPIB::18::INSTR"):
        self.smu = Keithley2450(address)
        self.smu.use_front_terminals()
        self.smu.reset()

    def iv_measurement(self, current_min=-1e-3, current_max=1e-3, data_points=10, measurements=10):
        """
        Performs an I-V curve measurement.
        """
        currents = np.linspace(current_min, current_max, data_points)
        voltages = np.zeros((data_points, measurements))

        for i, current in enumerate(currents):
            self.smu.ramp_to_current(current, steps=10, pause=1e-3)
            for j in range(measurements):
                voltages[i, j] = self.smu.voltage

        self.smu.shutdown()

        v_avg = np.mean(voltages, axis=1)
        plt.plot(v_avg, currents, 'ko')
        plt.xlabel("Voltage (V)")
        plt.ylabel("Current (A)")
        plt.title("I-V Curve")
        plt.show()

        return v_avg, currents
