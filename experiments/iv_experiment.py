import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from pymeasure.experiment.parameters import FloatParameter, IntegerParameter
from pymeasure.experiment.procedure import Procedure
from pymeasure.experiment.results import Results
from pymeasure.experiment.workers import Worker
from instruments.keithley_2450 import Keithley2450Instrument

class IVExperiment(Procedure):
    data_points = IntegerParameter("Data Points", units=None, minimum=10, maximum=10000, default=100)
    measurements = IntegerParameter("Number of Measurements", units=None, minimum=1, maximum=100, default=10)
    current_min = FloatParameter("Minimum Current", units="A", minimum=-1.05, maximum=0, default=-1e-3)
    current_max = FloatParameter("Maximum Current", units="A", minimum=0, maximum=1.05, default=1e-3)

    def execute(self):
        keithley = Keithley2450Instrument()
        currents = np.linspace(self.current_min, self.current_max, self.data_points)
        voltages = np.zeros((self.data_points, self.measurements))
        
        fig, ax = plt.subplots()
        line, = ax.plot([], [], 'ko-')
        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (A)")
        ax.set_title("Live I-V Curve Measurement")

        def update(frame):
            i = frame // self.measurements
            j = frame % self.measurements
            if i < self.data_points:
                if j == 0:
                    keithley.smu.ramp_to_current(currents[i], steps=10, pause=1e-3)
                voltages[i, j] = keithley.smu.voltage
                if j == self.measurements - 1:
                    v_avg = np.mean(voltages[:i+1], axis=1)
                    line.set_data(v_avg, currents[:i+1])
                    ax.relim()
                    ax.autoscale_view()
            return line,

        ani = FuncAnimation(fig, update, frames=self.data_points * self.measurements, blit=True, interval=50)
        plt.show()

        v_avg = np.mean(voltages, axis=1)
        keithley.smu.shutdown()

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"IVExperiment_Results_{now}.csv"
        with open(filename, "w") as f:
            f.write("Voltage (V), Current (A)\n")
            for v, i in zip(v_avg, currents):
                f.write(f"{v},{i}\n")
        print(f"Results saved to {filename}")

def run_iv_experiment():
    experiment = IVExperiment()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"IVExperiment_Results_{now}.csv"
    results = Results(experiment, filename)
    worker = Worker(results)
    worker.start()
    worker.join()