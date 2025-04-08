# import numpy as np
# import matplotlib.pyplot as plt
# from datetime import datetime
# from pymeasure.experiment.parameters import FloatParameter, IntegerParameter
# from pymeasure.experiment.procedure import Procedure
# from pymeasure.experiment.results import Results
# from pymeasure.experiment.workers import Worker
# from keithley_2450 import Keithley2450Instrument

# class IVExperiment(Procedure):
#     data_points = IntegerParameter("Data Points", units=None, minimum=10, maximum=10000, default=100)
#     measurements = IntegerParameter("Number of Measurements", units=None, minimum=1, maximum=100, default=10)
#     current_min = FloatParameter("Minimum Current", units="A", minimum=-1.05, maximum=0, default=-1e-3)
#     current_max = FloatParameter("Maximum Current", units="A", minimum=0, maximum=1.05, default=1e-3)

#     def execute(self):
#         keithley = Keithley2450Instrument()
#         voltages, currents = keithley.iv_measurement(
#             current_min=self.current_min,
#             current_max=self.current_max,
#             data_points=self.data_points,
#             measurements=self.measurements
#         )

#         # Save results
#         now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"IVExperiment_Results_{now}.csv"
#         np.savetxt(filename, np.column_stack([voltages, currents]), delimiter=",", header="Voltage (V), Current (A)")
#         print(f"Results saved to {filename}")

#         # Plot results
#         plt.plot(voltages, currents, 'ko-')
#         plt.xlabel("Voltage (V)")
#         plt.ylabel("Current (A)")
#         plt.title("I-V Measurement")
#         plt.show()

# # Run the experiment
# def run_iv_experiment():
#     experiment = IVExperiment()
#     now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     filename = f"IVExperiment_Results_{now}.csv"
#     results = Results(experiment, filename)
#     worker = Worker(results)
#     worker.start()
#     worker.join()

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
    # New sweep mode: “Current” or “Voltage”
    sweep_mode = Parameter("Sweep Mode", default="Current")
    # Parameters for current-sweep mode (sourcing current & measuring voltage)
    current_min = FloatParameter("Minimum Current", units="A", minimum=-1.05, maximum=0, default=-1e-3)
    current_max = FloatParameter("Maximum Current", units="A", minimum=0, maximum=1.05, default=1e-3)
    # Parameters for voltage-sweep mode (sourcing voltage & measuring current)
    voltage_min = FloatParameter("Minimum Voltage", units="V", minimum=-1.05, maximum=0, default=-1e-3)
    voltage_max = FloatParameter("Maximum Voltage", units="V", minimum=0, maximum=1.05, default=1e-3)

    def execute(self):
        keithley = Keithley2450Instrument()
        if self.sweep_mode.lower() == "current":
            x_values, y_values = keithley.iv_measurement_current(
                current_min=self.current_min,
                current_max=self.current_max,
                data_points=self.data_points,
                measurements=self.measurements
            )
            # For a current sweep, the independent variable is the current.
            header = "Current (A), Voltage (V)\n"
        elif self.sweep_mode.lower() == "voltage":
            x_values, y_values = keithley.iv_measurement_voltage(
                voltage_min=self.voltage_min,
                voltage_max=self.voltage_max,
                data_points=self.data_points,
                measurements=self.measurements
            )
            # For a voltage sweep, the independent variable is the voltage.
            header = "Voltage (V), Current (A)\n"
        else:
            raise ValueError("Invalid Sweep Mode. Choose 'Current' or 'Voltage'.")

        # Save results with an appropriate header
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"IVExperiment_Results_{now}.csv"
        with open(filename, "w") as f:
            f.write(header)
            for x, y in zip(x_values, y_values):
                f.write(f"{x},{y}\n")

        print(f"Results saved to {filename}")

# Run the experiment
def run_iv_experiment():
    experiment = IVExperiment()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"IVExperiment_Results_{now}.csv"
    results = Results(experiment, filename)
    worker = Worker(results)
    worker.start()
    worker.join()
