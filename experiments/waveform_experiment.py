from datetime import datetime
from pymeasure.experiment.parameters import FloatParameter, IntegerParameter
from pymeasure.experiment.procedure import Procedure
from pymeasure.experiment.results import Results
from pymeasure.experiment.workers import Worker
from instruments.keithley_6221 import Keithley6221Instrument

class WaveformExperiment(Procedure):
    amplitude = FloatParameter("Amplitude", units="A", minimum=2e-12, maximum=0.105, default=0.05)
    frequency = FloatParameter("Frequency", units="Hz", minimum=1e-3, maximum=1e5, default=100)
    duty_cycle = FloatParameter("Duty Cycle", units="%", minimum=0, maximum=100, default=50)
    duration_cycles = IntegerParameter("Duration Cycles", units="cycles", minimum=1, maximum=10000, default=10)

    def execute(self):
        keithley = Keithley6221Instrument()
        results = keithley.generate_waveform(
            amplitude=self.amplitude,
            frequency=self.frequency,
            duty_cycle=self.duty_cycle,
            duration_cycles=self.duration_cycles
        )

        # Save results
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"WaveformExperiment_Results_{now}.csv"
        with open(filename, "w") as f:
            for key, value in results.items():
                f.write(f"{key},{value}\n")
        print(f"Results saved to {filename}")

# Run the experiment
def run_waveform_experiment():
    experiment = WaveformExperiment()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"WaveformExperiment_Results_{now}.csv"
    results = Results(experiment, filename)
    worker = Worker(results)
    worker.start()
    worker.join()
