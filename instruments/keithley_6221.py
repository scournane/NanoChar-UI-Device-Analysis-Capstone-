from pymeasure.instruments.keithley import Keithley6221
from pymeasure.instruments.resources import list_resources
from pymeasure.adapters import VISAAdapter
import time

class Keithley6221Instrument:
    def __init__(self, address="GPIB0::12::INSTR", timeout=50000):
        # Check available instruments before initializing
        available_resources = list_resources()
        if address not in available_resources:
            raise ValueError(f"Keithley 6221 not found at {address}. Available: {available_resources}")

        self.adapter = VISAAdapter(address, timeout=timeout)
        self.source = Keithley6221(self.adapter)

        # Ensure instrument is ready
        self.source.clear()

        # Beep test to confirm successful connection
        try:
            self.source.beep(frequency=700, duration=1.0)  # 700 Hz beep for 1 second
            print("Keithley 6221 Connected - Beep!")
        except Exception as e:
            print(f"Beep test failed: {e}")

    def generate_waveform(self, amplitude=0.05, frequency=100, duty_cycle=50, duration_cycles=10):
        """
        Generates a square waveform using Keithley 6221.
        Parameters:
            amplitude (float): Amplitude of the waveform (A).
            frequency (float): Frequency of the waveform (Hz).
            duty_cycle (float): Duty cycle of the waveform (%).
            duration_cycles (int): Number of waveform cycles.
        Returns:
            dict: Contains waveform parameters and confirmation.
        """
        self.source.waveform_function = "square"
        self.source.waveform_amplitude = amplitude
        self.source.waveform_frequency = frequency
        self.source.waveform_dutycycle = duty_cycle
        self.source.waveform_duration_cycles = duration_cycles
        self.source.waveform_arm()
        self.source.waveform_start()

        # Wait for waveform to complete
        try:
            self.source.adapter.wait_for_srq(timeout=30)
        except Exception as e:
            print(f"Timeout or error waiting for SRQ: {e}")

        self.source.waveform_abort()

        return {
            "Amplitude": amplitude,
            "Frequency": frequency,
            "Duty Cycle": duty_cycle,
            "Duration Cycles": duration_cycles,
            "Status": "Waveform Completed"
        }

