import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from pymeasure.experiment.parameters import IntegerParameter, FloatParameter
from pymeasure.experiment.procedure import Procedure
from pymeasure.experiment.results import Results
from pymeasure.experiment.workers import Worker
from instruments.keithley_2182a import Keithley2182Instrument

class NanoVoltExperiment(Procedure):
    samples = IntegerParameter("Number of Samples", units="samples", minimum=1, maximum=10000, default=100)
    nplc = FloatParameter("NPLC", units="", minimum=0.01, maximum=10, default=5)

    def execute(self):
        keithley = Keithley2182Instrument()
        voltages = np.zeros(self.samples)

        fig, ax = plt.subplots()
        line, = ax.plot([], [], 'bo-')
        ax.set_xlabel("Sample Number")
        ax.set_ylabel("Voltage (V)")
        ax.set_title("Live Nanovoltmeter Readings")
        ax.grid(True)

        def update(frame):
            if frame < self.samples:
                voltages[frame] = keithley.nano.voltage_nplc
                line.set_data(np.arange(frame + 1), voltages[:frame + 1])
                ax.relim()
                ax.autoscale_view()
            return line,

        ani = FuncAnimation(fig, update, frames=self.samples, blit=True, interval=100)
        plt.show()

        avg_voltage = np.mean(voltages)
        std_voltage = np.std(voltages)

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"NanoVoltExperiment_Results_{now}.csv"
        with open(filename, "w") as f:
            f.write(f"Average Voltage,{avg_voltage}\n")
            f.write(f"Std Dev,{std_voltage}\n")
            f.write(f"Samples,{self.samples}\n")
        print(f"Results saved to {filename}")

def run_nanovolt_experiment():
    experiment = NanoVoltExperiment()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"NanoVoltExperiment_Results_{now}.csv"
    results = Results(experiment, filename)
    worker = Worker(results)
    worker.start()
    worker.join()