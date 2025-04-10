
from pymeasure.instruments.keithley import Keithley2450
from pymeasure.instruments.resources import list_resources
from pymeasure.adapters import VISAAdapter

class Keithley2450Instrument:
    def __init__(self, address="GPIB0::18::INSTR", timeout=50000):
        # Check available instruments before initializing
        available_resources = list_resources()
        if address not in available_resources:
            raise ValueError(f"Keithley 2450 not found at {address}. Available: {available_resources}")

        self.adapter = VISAAdapter(address, timeout=timeout)
        self.smu = Keithley2450(self.adapter)

        # Test connection with a beep
        self.smu.beep(frequency=90, duration=1.0)
        print("Keithley 2450 Connected - Beep!")

    def iv_measurement(self, current_min=-1e-3, current_max=1e-3, data_points=10, measurements=10):
        """
        Performs an I-V curve measurement.
        """
        import numpy as np
        import matplotlib.pyplot as plt

        currents = np.linspace(current_min, current_max, data_points)
        voltages = np.zeros((data_points, measurements))

        for i, current in enumerate(currents):
            self.smu.ramp_to_current(current, steps=10, pause=1e-3)
            for j in range(measurements):
                voltages[i, j] = self.smu.voltage

        self.smu.shutdown()
        v_avg = np.mean(voltages, axis=1)

        plt.plot(v_avg, currents, 'ko-')
        plt.xlabel("Voltage (V)")
        plt.ylabel("Current (A)")
        plt.title("I-V Curve Measurement")
        plt.show()

        return v_avg, currents