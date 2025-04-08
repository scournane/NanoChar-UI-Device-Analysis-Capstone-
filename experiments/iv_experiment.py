import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from pymeasure.experiment.parameters import FloatParameter, IntegerParameter, Parameter
from pymeasure.experiment.procedure import Procedure
from pymeasure.experiment.results import Results
from pymeasure.experiment.workers import Worker
from instruments.keithley_2450 import Keithley2450Instrument

class IVExperiment(Procedure):
    data_points = IntegerParameter("Data Points", units=None, minimum=10, maximum=10000, default=100)
    measurements = IntegerParameter("Number of Measurements", units=None, minimum=1, maximum=100, default=10)
    
    # Sweep Mode: "Current" or "Voltage"
    sweep_mode = Parameter("Sweep Mode", default="Current")
    
    # Parameters for current-sweep (sourcing current, measuring voltage)
    current_min = FloatParameter("Minimum Current", units="A", minimum=-1.05, maximum=0, default=-1e-3)
    current_max = FloatParameter("Maximum Current", units="A", minimum=0, maximum=1.05, default=1e-3)
    
    # Parameters for voltage-sweep (sourcing voltage, measuring current)
    voltage_min = FloatParameter("Minimum Voltage", units="V", minimum=-1.05, maximum=0, default=-1e-3)
    voltage_max = FloatParameter("Maximum Voltage", units="V", minimum=0, maximum=1.05, default=1e-3)

    def execute(self):
        keithley = Keithley2450Instrument()
        
        # Define a progress callback that emits "results" for real-time update.
        progress_callback = lambda data: self.emit("results", data)
        
        if self.sweep_mode.lower() == "current":
            # Using current-sweep: source current, measure voltage.
            x_values, y_values, y_std = keithley.iv_measurement_current(
                current_min=self.current_min,
                current_max=self.current_max,
                data_points=self.data_points,
                measurements=self.measurements,
                progress_callback=progress_callback
            )
            header = "Current (A), Voltage (V), Voltage Std (V)\n"
        elif self.sweep_mode.lower() == "voltage":
            # Using voltage-sweep: source voltage, measure current.
            x_values, y_values, y_std = keithley.iv_measurement_voltage(
                voltage_min=self.voltage_min,
                voltage_max=self.voltage_max,
                data_points=self.data_points,
                measurements=self.measurements,
                progress_callback=progress_callback
            )
            header = "Voltage (V), Current (A), Current Std (A)\n"
        else:
            raise ValueError("Invalid Sweep Mode. Choose 'Current' or 'Voltage'.")

        # Save final results to CSV.
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"IVExperiment_Results_{now}.csv"
        with open(filename, "w") as f:
            f.write(header)
            for x, y, s in zip(x_values, y_values, y_std):
                f.write(f"{x},{y},{s}\n")
        print(f"Results saved to {filename}")

# Run the experiment with real-time plotting.
def run_iv_experiment():
    experiment = IVExperiment()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"IVExperiment_Results_{now}.csv"
    results = Results(experiment, filename)
    # Import Plotter from PyMeasure to enable real-time plotting.
    from pymeasure.display import Plotter
    plotter = Plotter(results, refresh_time=0.1, linewidth=1)
    plotter.start()
    worker = Worker(results)
    worker.start()
    worker.join()
