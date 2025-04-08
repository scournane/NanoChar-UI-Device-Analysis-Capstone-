import tkinter
import customtkinter
import threading
from instruments.keithley_2450 import Keithley2450Instrument
from instruments.keithley_6221 import Keithley6221Instrument
from instruments.keithley_2182a import Keithley2182Instrument

# Set appearance and theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Create main application window
app = customtkinter.CTk()
app.geometry("1366x768")
app.resizable(False, False)
app.title("Nano - Device Window")

# Configure grid layout for the main window
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=0)
app.grid_columnconfigure(1, weight=0)
app.grid_columnconfigure(2, weight=1)

# ------------------------
# INSTRUMENTS PANEL
# ------------------------
frame_instruments = customtkinter.CTkFrame(app, width=300, height=700)
frame_instruments.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)

instruments_label = customtkinter.CTkLabel(frame_instruments, text="Instruments", font=('Arial', 16, 'bold'))
instruments_label.pack(pady=(10, 0))

# Textbox to display the instruments list
instruments_textbox = customtkinter.CTkTextbox(frame_instruments, width=280, height=400)
instruments_textbox.pack(pady=10)
instruments_textbox.configure(state="disabled")  # read-only

instruments_list = []  # Will store dictionaries: {"name": ..., "type": ...}

def refresh_instrument_display():
    instruments_textbox.configure(state="normal")
    instruments_textbox.delete("1.0", "end")
    for inst in instruments_list:
        instruments_textbox.insert("end", f"{inst['name']} - {inst['type']}\n")
    instruments_textbox.configure(state="disabled")

def add_instrument_to_list(inst_name, inst_type):
    instruments_list.append({"name": inst_name, "type": inst_type})
    print(f"Added instrument: {inst_name} of type {inst_type}")
    refresh_instrument_display()

def show_instrument_panel():
    inst_window = customtkinter.CTkToplevel(app)
    inst_window.geometry("400x200")
    inst_window.title("Add Instrument")
    inst_window.transient(app)
    inst_window.grab_set()
    inst_window.focus_force()

    label_name = customtkinter.CTkLabel(inst_window, text="Instrument Name:")
    label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_name = customtkinter.CTkEntry(inst_window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    label_type = customtkinter.CTkLabel(inst_window, text="Select Instrument:")
    label_type.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    combobox_type = customtkinter.CTkComboBox(inst_window, values=["Keithley 2450", "Keithley 6221", "Keithley 2182A"])
    combobox_type.grid(row=1, column=1, padx=10, pady=10)

    def add_instrument():
        inst_name = entry_name.get()
        inst_type = combobox_type.get()
        if inst_name and inst_type:
            add_instrument_to_list(inst_name, inst_type)
            inst_window.destroy()
        else:
            print("Please provide both name and type.")

    button_add = customtkinter.CTkButton(inst_window, text="Add", command=add_instrument)
    button_add.grid(row=2, column=0, padx=10, pady=10)
    button_cancel = customtkinter.CTkButton(inst_window, text="Cancel", command=inst_window.destroy)
    button_cancel.grid(row=2, column=1, padx=10, pady=10)

button_add_instrument = customtkinter.CTkButton(frame_instruments, text="Add Instrument", command=show_instrument_panel)
button_add_instrument.pack(pady=10)

# ------------------------
# EXPERIMENTS PANEL
# ------------------------
frame_experiments = customtkinter.CTkFrame(app, width=300, height=700)
frame_experiments.grid(row=0, column=1, sticky="ns", padx=(5, 5), pady=10)

experiment_label = customtkinter.CTkLabel(frame_experiments, text="Experiments", font=('Arial', 16, 'bold'))
experiment_label.pack(pady=(10, 0))

# Textbox to display the experiments list
experiments_textbox = customtkinter.CTkTextbox(frame_experiments, width=280, height=400)
experiments_textbox.pack(pady=10)
experiments_textbox.configure(state="disabled")  # read-only

experiments_list = []  # Will store dictionaries: {"name": ..., "instrument": ...}

def refresh_experiment_display():
    experiments_textbox.configure(state="normal")
    experiments_textbox.delete("1.0", "end")
    for exp in experiments_list:
        experiments_textbox.insert("end", f"{exp['name']} - {exp['instrument']}\n")
    experiments_textbox.configure(state="disabled")

def add_experiment_to_list(exp_name, instrument_name):
    experiments_list.append({"name": exp_name, "instrument": instrument_name})
    print(f"Added experiment: {exp_name} linked to instrument {instrument_name}")
    refresh_experiment_display()   # Update the display in the experiments panel
    refresh_experiment_combobox()  # Also update the combobox used for selecting an experiment

def show_experiment_panel():
    exp_window = customtkinter.CTkToplevel(app)
    exp_window.geometry("400x200")
    exp_window.title("Add Experiment")
    exp_window.transient(app)
    exp_window.grab_set()
    exp_window.focus_force()

    label_name = customtkinter.CTkLabel(exp_window, text="Experiment Name:")
    label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_name = customtkinter.CTkEntry(exp_window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    label_inst = customtkinter.CTkLabel(exp_window, text="Select Instrument:")
    label_inst.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    inst_names = [inst['name'] for inst in instruments_list] if instruments_list else ["No instruments available"]
    combobox_inst = customtkinter.CTkComboBox(exp_window, values=inst_names)
    combobox_inst.grid(row=1, column=1, padx=10, pady=10)

    def add_experiment():
        exp_name = entry_name.get()
        inst_name = combobox_inst.get()
        if exp_name and inst_name and inst_name != "No instruments available":
            add_experiment_to_list(exp_name, inst_name)
            exp_window.destroy()
        else:
            print("Please provide experiment name and select a valid instrument.")

    button_add = customtkinter.CTkButton(exp_window, text="Add", command=add_experiment)
    button_add.grid(row=2, column=0, padx=10, pady=10)
    button_cancel = customtkinter.CTkButton(exp_window, text="Cancel", command=exp_window.destroy)
    button_cancel.grid(row=2, column=1, padx=10, pady=10)

add_experiment_button = customtkinter.CTkButton(frame_experiments, text="Add Experiment", command=show_experiment_panel)
add_experiment_button.pack(pady=10)

# ------------------------
# CONTROLS PANEL (Run Experiments)
# ------------------------
frame_controls = customtkinter.CTkFrame(app, width=300, height=100)
frame_controls.grid(row=2, column=1, sticky="ns", padx=10, pady=10)

# Combobox for selecting an experiment (populated from experiments_list)
combobox_exp_select = customtkinter.CTkComboBox(frame_controls, values=[exp['name'] for exp in experiments_list])
combobox_exp_select.pack(pady=5)

def refresh_experiment_combobox():
    new_values = [exp['name'] for exp in experiments_list]
    combobox_exp_select.configure(values=new_values)

def start_experiment(exp_name):
    # Find the experiment details by name
    experiment = next((exp for exp in experiments_list if exp['name'] == exp_name), None)
    if not experiment:
        print("Experiment not found!")
        return

    # Find the instrument details by name
    instrument = next((inst for inst in instruments_list if inst['name'] == experiment['instrument']), None)
    if not instrument:
        print("Instrument not found!")
        return

    def run_experiment():
        try:
            if instrument['type'] == "Keithley 2450":
                print("Running I-V measurement on Keithley 2450...")
                keithley = Keithley2450Instrument()
                # Default: current sweep if launched from experiments list
                keithley.iv_measurement_current()
            elif instrument['type'] == "Keithley 6221":
                print("Running waveform generation on Keithley 6221...")
                keithley = Keithley6221Instrument()
                keithley.generate_waveform()
            elif instrument['type'] == "Keithley 2182A":
                print("Running nanovoltage measurement on Keithley 2182A...")
                keithley = Keithley2182Instrument()
                keithley.measure_nanovoltage()
            else:
                print("Unknown instrument type.")
        except Exception as e:
            print(f"Error during experiment: {e}")

    # Run the experiment in a background thread so the UI remains responsive
    threading.Thread(target=run_experiment).start()

button_run_exp = customtkinter.CTkButton(frame_controls, text="Run Experiment", 
                                         command=lambda: start_experiment(combobox_exp_select.get()))
button_run_exp.pack(pady=10)

# ------------------------
# IV EXPERIMENT PANEL
# ------------------------
def show_iv_experiment_panel():
    iv_window = customtkinter.CTkToplevel(app)
    iv_window.geometry("500x450")
    iv_window.title("IV Experiment Parameters")
    iv_window.transient(app)
    iv_window.grab_set()

    # Sweep Mode Selection
    label_sweep_mode = customtkinter.CTkLabel(iv_window, text="Sweep Mode:")
    label_sweep_mode.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    combobox_sweep_mode = customtkinter.CTkComboBox(iv_window, values=["Current Sweep", "Voltage Sweep"])
    combobox_sweep_mode.grid(row=0, column=1, padx=10, pady=10)
    combobox_sweep_mode.set("Current Sweep")  # default selection

    # Data Points
    label_data_points = customtkinter.CTkLabel(iv_window, text="Data Points:")
    label_data_points.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_data_points = customtkinter.CTkEntry(iv_window)
    entry_data_points.grid(row=1, column=1, padx=10, pady=10)
    entry_data_points.insert(0, "100")

    # Measurements per Point
    label_measurements = customtkinter.CTkLabel(iv_window, text="Measurements per Point:")
    label_measurements.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_measurements = customtkinter.CTkEntry(iv_window)
    entry_measurements.grid(row=2, column=1, padx=10, pady=10)
    entry_measurements.insert(0, "10")

    # Parameters for Current Sweep
    label_current_min = customtkinter.CTkLabel(iv_window, text="Min Current (A):")
    label_current_min.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_current_min = customtkinter.CTkEntry(iv_window)
    entry_current_min.grid(row=3, column=1, padx=10, pady=10)
    entry_current_min.insert(0, "-0.001")

    label_current_max = customtkinter.CTkLabel(iv_window, text="Max Current (A):")
    label_current_max.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_current_max = customtkinter.CTkEntry(iv_window)
    entry_current_max.grid(row=4, column=1, padx=10, pady=10)
    entry_current_max.insert(0, "0.001")
    
    # Note for current fields; appears when these fields are disabled
    label_current_note = customtkinter.CTkLabel(iv_window, text="", fg_color="transparent", text_color="red")
    label_current_note.grid(row=3, column=2, rowspan=2, padx=10, pady=10)

    # Parameters for Voltage Sweep
    label_voltage_min = customtkinter.CTkLabel(iv_window, text="Min Voltage (V):")
    label_voltage_min.grid(row=5, column=0, padx=10, pady=10, sticky="e")
    entry_voltage_min = customtkinter.CTkEntry(iv_window)
    entry_voltage_min.grid(row=5, column=1, padx=10, pady=10)
    entry_voltage_min.insert(0, "-0.001")

    label_voltage_max = customtkinter.CTkLabel(iv_window, text="Max Voltage (V):")
    label_voltage_max.grid(row=6, column=0, padx=10, pady=10, sticky="e")
    entry_voltage_max = customtkinter.CTkEntry(iv_window)
    entry_voltage_max.grid(row=6, column=1, padx=10, pady=10)
    entry_voltage_max.insert(0, "0.001")

    # Note for voltage fields; appears when these fields are disabled
    label_voltage_note = customtkinter.CTkLabel(iv_window, text="", fg_color="transparent", text_color="red")
    label_voltage_note.grid(row=5, column=2, rowspan=2, padx=10, pady=10)

    # Callback to update entry states based on the selected sweep mode
    def on_sweep_mode_change(event=None):
        mode = combobox_sweep_mode.get()
        if mode == "Current Sweep":
            entry_current_min.configure(state="normal")
            entry_current_max.configure(state="normal")
            entry_voltage_min.configure(state="disabled")
            entry_voltage_max.configure(state="disabled")
            label_voltage_note.configure(text="Disabled: Only valid in Voltage Sweep")
            label_current_note.configure(text="")  # Clear note
        elif mode == "Voltage Sweep":
            entry_voltage_min.configure(state="normal")
            entry_voltage_max.configure(state="normal")
            entry_current_min.configure(state="disabled")
            entry_current_max.configure(state="disabled")
            label_current_note.configure(text="Disabled: Only valid in Current Sweep")
            label_voltage_note.configure(text="")  # Clear note

    combobox_sweep_mode.bind("<<ComboboxSelected>>", on_sweep_mode_change)
    on_sweep_mode_change()  # initialize states based on default selection

    def run_iv_experiment_from_ui():
        try:
            data_points = int(entry_data_points.get())
            measurements = int(entry_measurements.get())
        except ValueError:
            print("Invalid input for data points or measurements. Please enter valid numbers.")
            return

        sweep_mode = combobox_sweep_mode.get()
        if sweep_mode == "Current Sweep":
            try:
                current_min = float(entry_current_min.get())
                current_max = float(entry_current_max.get())
            except ValueError:
                print("Invalid input for current parameters. Please enter valid numbers.")
                return
            try:
                keithley = Keithley2450Instrument()
                x_values, y_values = keithley.iv_measurement_current(
                    current_min=current_min,
                    current_max=current_max,
                    data_points=data_points,
                    measurements=measurements
                )
            except Exception as e:
                print(f"Error running IV measurement (current sweep): {e}")
                return
            header = "Current (A), Voltage (V)\n"
        elif sweep_mode == "Voltage Sweep":
            try:
                voltage_min = float(entry_voltage_min.get())
                voltage_max = float(entry_voltage_max.get())
            except ValueError:
                print("Invalid input for voltage parameters. Please enter valid numbers.")
                return
            try:
                keithley = Keithley2450Instrument()
                x_values, y_values = keithley.iv_measurement_voltage(
                    voltage_min=voltage_min,
                    voltage_max=voltage_max,
                    data_points=data_points,
                    measurements=measurements
                )
            except Exception as e:
                print(f"Error running IV measurement (voltage sweep): {e}")
                return
            header = "Voltage (V), Current (A)\n"
        else:
            print("Invalid sweep mode selected.")
            return

        # Save the results to a CSV file
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"IVExperiment_Results_{now}.csv"
        try:
            with open(filename, "w") as f:
                f.write(header)
                for x, y in zip(x_values, y_values):
                    f.write(f"{x},{y}\n")
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")

        iv_window.destroy()  # Close the IV experiment window when done

    button_run_iv = customtkinter.CTkButton(iv_window, text="Run IV Experiment", command=run_iv_experiment_from_ui)
    button_run_iv.grid(row=7, column=0, columnspan=3, padx=10, pady=20)

button_iv_experiment = customtkinter.CTkButton(frame_controls, text="IV Experiment", command=show_iv_experiment_panel)
button_iv_experiment.pack(pady=10)

# Start the main event loop
app.mainloop()
