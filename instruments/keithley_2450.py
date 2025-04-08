from pymeasure.instruments.keithley import Keithley2450
from pymeasure.instruments.resources import list_resources
from pymeasure.adapters import VISAAdapter

class Keithley2450Instrument:
    def __init__(self, address="GPIB0::18::INSTR", timeout=50000):
        # Check available instruments before initializing.
        available_resources = list_resources()
        if address not in available_resources:
            raise ValueError(f"Keithley 2450 not found at {address}. Available: {available_resources}")

        self.adapter = VISAAdapter(address, timeout=timeout)
        self.smu = Keithley2450(self.adapter)

        # Test connection with a beep.
        self.smu.beep(frequency=90, duration=1.0)
        print("Keithley 2450 Connected - Beep!")

    def iv_measurement_current(self, current_min=-1e-3, current_max=1e-3, data_points=10, measurements=10, progress_callback=None):
        """
        Performs an I–V measurement by sourcing current and measuring voltage.
        For each setpoint the method obtains multiple voltage readings, calculates the mean and standard deviation,
        and calls the provided progress_callback with the current result.
        Returns a tuple: (currents, averaged voltages, voltage standard deviations)
        """
        import numpy as np

        currents = np.linspace(current_min, current_max, data_points)
        voltages = np.zeros((data_points, measurements))
        avg_list = []
        std_list = []

        for i, current in enumerate(currents):
            self.smu.ramp_to_current(current, steps=10, pause=1e-3)
            for j in range(measurements):
                voltages[i, j] = self.smu.voltage
            avg_voltage = np.mean(voltages[i, :])
            std_voltage = np.std(voltages[i, :])
            avg_list.append(avg_voltage)
            std_list.append(std_voltage)
            if progress_callback:
                progress_callback({
                    "Current (A)": current,
                    "Voltage (V)": avg_voltage,
                    "Voltage Std (V)": std_voltage
                })
        self.smu.shutdown()
        return currents, np.array(avg_list), np.array(std_list)

    def iv_measurement_voltage(self, voltage_min=-1e-3, voltage_max=1e-3, data_points=10, measurements=10, progress_callback=None):
        """
        Performs an I–V measurement by sourcing voltage and measuring current.
        For each setpoint the method obtains multiple current readings, calculates the mean and standard deviation,
        and calls the provided progress_callback with the current result.
        Returns a tuple: (voltages, averaged currents, current standard deviations)
        """
        import numpy as np

        voltages = np.linspace(voltage_min, voltage_max, data_points)
        currents = np.zeros((data_points, measurements))
        avg_list = []
        std_list = []

        for i, voltage in enumerate(voltages):
            self.smu.ramp_to_voltage(voltage, steps=10, pause=1e-3)
            for j in range(measurements):
                currents[i, j] = self.smu.current
            avg_current = np.mean(currents[i, :])
            std_current = np.std(currents[i, :])
            avg_list.append(avg_current)
            std_list.append(std_current)
            if progress_callback:
                progress_callback({
                    "Voltage (V)": voltage,
                    "Current (A)": avg_current,
                    "Current Std (A)": std_current
                })
        self.smu.shutdown()
        return voltages, np.array(avg_list), np.array(std_list)
