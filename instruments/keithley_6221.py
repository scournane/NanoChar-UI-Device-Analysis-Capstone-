import numpy as np
import matplotlib.pyplot as plt
from pymeasure.instruments.keithley import Keithley6221

class Keithley6221Instrument:
    def __init__(self, address="GPIB::15"):
        self.source = Keithley6221(address)
        self.source.clear()

    def generate_waveform(self, amplitude=0.05, frequency=100, duty_cycle=50, duration_cycles=10):
        """
        Generates a square waveform signal.
        """
        self.source.waveform_function = "square"
        self.source.waveform_amplitude = amplitude
        self.source.waveform_frequency = frequency
        self.source.waveform_dutycycle = duty_cycle
        self.source.waveform_duration_cycles = duration_cycles
        self.source.waveform_arm()
        self.source.waveform_start()
        self.source.adapter.wait_for_srq(timeout=30)
        self.source.waveform_abort()

        return {
            "Amplitude": amplitude,
            "Frequency": frequency,
            "Duty Cycle": duty_cycle,
            "Duration Cycles": duration_cycles,
            "Status": "Waveform Completed"
        }
