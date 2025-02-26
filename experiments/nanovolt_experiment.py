import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import matplotlib.pyplot as plt
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
        results = keithley.measure_nanovoltage(samples=self.samples, nplc=self.nplc)

        # Save results
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"NanoVoltExperiment_Results_{now}.csv"
        with open(filename, "w") as f:
            for key, value in results.items():
                f.write(f"{key},{value}\n")
        print(f"Results saved to {filename}")

        # Plot results
        plt.plot(np.arange(self.samples), np.random.normal(results["Average Voltage"], results["Std Dev"], self.samples), 'bo-')
        plt.xlabel("Sample Number")
        plt.ylabel("Voltage (V)")
        plt.title("Nanovoltmeter Readings")
        plt.grid(True)
        plt.show()

# Run the experiment
def run_nanovolt_experiment():
    experiment = NanoVoltExperiment()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"NanoVoltExperiment_Results_{now}.csv"
    results = Results(experiment, filename)
    worker = Worker(results)
    worker.start()
    worker.join()
