import tkinter
import customtkinter
import time
import threading
from instruments.keithley_2450 import Keithley2450Instrument
from instruments.keithley_6221 import Keithley6221Instrument
from instruments.keithley_2182a import Keithley2182Instrument

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("1366x768")
app.resizable(False, False)
app.title("Nano - Device Window")

# Configure grid for main app window
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=0)
app.grid_columnconfigure(1, weight=0)
app.grid_columnconfigure(2, weight=1)

# ===================================================================
# INSTRUMENTS COLUMN (Left Panel)
frame_instruments = customtkinter.CTkFrame(app, width=300, height=700)
frame_instruments.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)

instruments_label = customtkinter.CTkLabel(frame_instruments, text="Instruments", font=('Arial', 16, 'bold'))
instruments_label.pack(pady=(10, 0))

instruments_list = []

def show_panel():
    inst_window = customtkinter.CTkToplevel(app)
    inst_window.geometry("400x500")
    inst_window.title("Add Instrument")

    # Ensure the window stays on top
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
        instruments_list.append({"name": entry_name.get(), "type": combobox_type.get()})
        inst_window.destroy()

    button_add = customtkinter.CTkButton(inst_window, text="Add", command=add_instrument)
    button_add.grid(row=2, column=0, padx=10, pady=20)
    button_cancel = customtkinter.CTkButton(inst_window, text="Cancel", command=inst_window.destroy)
    button_cancel.grid(row=2, column=1, padx=10, pady=20)

button_add_instrument = customtkinter.CTkButton(master=frame_instruments, text="Add Instrument", command=show_panel)
button_add_instrument.pack(pady=10)

# ===================================================================
# EXPERIMENTS COLUMN (Middle Panel)
frame_experiments = customtkinter.CTkFrame(app, width=300, height=700)
frame_experiments.grid(row=0, column=1, sticky="ns", padx=(5, 5), pady=10)

experiment_label = customtkinter.CTkLabel(frame_experiments, text="Experiments", font=('Arial', 16, 'bold'))
experiment_label.pack(pady=(10, 0))

experiments_list = []

def show_experiment_panel():
    exp_window = customtkinter.CTkToplevel(app)
    exp_window.geometry("400x500")
    exp_window.title("Add Experiment")

    # Ensure the window stays on top
    exp_window.transient(app)
    exp_window.grab_set()
    exp_window.focus_force()

    label_name = customtkinter.CTkLabel(exp_window, text="Experiment Name:")
    label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_name = customtkinter.CTkEntry(exp_window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    label_inst = customtkinter.CTkLabel(exp_window, text="Select Instrument:")
    label_inst.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    combobox_inst = customtkinter.CTkComboBox(exp_window, values=[inst['name'] for inst in instruments_list])
    combobox_inst.grid(row=1, column=1, padx=10, pady=10)

    def add_experiment():
        experiments_list.append({"name": entry_name.get(), "instrument": combobox_inst.get()})
        exp_window.destroy()

    button_add = customtkinter.CTkButton(exp_window, text="Add", command=add_experiment)
    button_add.grid(row=2, column=0, padx=10, pady=20)
    button_cancel = customtkinter.CTkButton(exp_window, text="Cancel", command=exp_window.destroy)
    button_cancel.grid(row=2, column=1, padx=10, pady=20)

add_experiment_button = customtkinter.CTkButton(master=frame_experiments, text="Add Experiment", command=show_experiment_panel)
add_experiment_button.pack(pady=10)

# ===================================================================
# RUNNING EXPERIMENTS
def start_experiment(exp_name):
    experiment = next((exp for exp in experiments_list if exp['name'] == exp_name), None)
    if not experiment:
        print("Experiment not found!")
        return
    
    instrument = next((inst for inst in instruments_list if inst['name'] == experiment['instrument']), None)
    if not instrument:
        print("Instrument not found!")
        return

    def run_experiment():
        if instrument['type'] == "Keithley 2450":
            keithley = Keithley2450Instrument()
            keithley.iv_measurement()
        elif instrument['type'] == "Keithley 6221":
            keithley = Keithley6221Instrument()
            keithley.generate_waveform()
        elif instrument['type'] == "Keithley 2182A":
            keithley = Keithley2182Instrument()
            keithley.measure_nanovoltage()

    threading.Thread(target=run_experiment).start()

frame_controls = customtkinter.CTkFrame(app, width=300, height=100)
frame_controls.grid(row=2, column=1, sticky="ns", padx=10, pady=10)

combobox_exp_select = customtkinter.CTkComboBox(frame_controls, values=[exp['name'] for exp in experiments_list])
combobox_exp_select.pack(pady=5)

button_run_exp = customtkinter.CTkButton(frame_controls, text="Run Experiment", 
                                         command=lambda: start_experiment(combobox_exp_select.get()))
button_run_exp.pack(pady=10)

app.mainloop()
