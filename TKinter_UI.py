import tkinter
import customtkinter
import time

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window 
app.geometry("1366x768")
app.resizable(False, False)
app.title("Nano - Device Window")

# Configure grid for main app window
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=0)  # Instruments column
app.grid_columnconfigure(1, weight=0)  # Experiments column
app.grid_columnconfigure(2, weight=1)  # Tabview column expands

def button_function():
    print("button pressed")


# ===================================================================
# TABVIEW ON THE RIGHT
tabview = customtkinter.CTkTabview(master=app, width=1000, height=800, anchor='w', corner_radius=10)
tabview.grid(row=0, column=2, sticky="nsew")

# Tabs
TABsettings = tabview.add("Settings")  
TABtable = tabview.add("Table")
TABgraph = tabview.add("Graph")  
tabview.set("Settings")  # set currently visible tab


# ===================================================================
# INSTRUMENTS COLUMN (Left Column)
frame_instruments = customtkinter.CTkFrame(app, width=300, height=700)
frame_instruments.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)

instruments_label = customtkinter.CTkLabel(frame_instruments, text="Instruments", font=('Arial', 16, 'bold'))
instruments_label.pack(pady=(10, 0))

# "Add Instrument" Button
def show_panel():
    # Create a Toplevel window for the pop-up
    inst_window = customtkinter.CTkToplevel(app)
    inst_window.geometry("400x500")
    inst_window.title("Add Instrument")

    # Bring the window to the front
    inst_window.transient(app)  # On top of main window
    inst_window.grab_set()      # Modal
    inst_window.focus_force()

    # Instrument Name
    label_name = customtkinter.CTkLabel(inst_window, text="Instrument Name:")
    label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_name = customtkinter.CTkEntry(inst_window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    # Voltage Type Combobox
    label_voltage_type = customtkinter.CTkLabel(inst_window, text="Voltage Type:")
    label_voltage_type.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    combobox_voltage_type = customtkinter.CTkComboBox(inst_window, values=["DC Voltage", "AC Voltage"])
    combobox_voltage_type.set("DC Voltage")
    combobox_voltage_type.grid(row=1, column=1, padx=10, pady=10)

    # Sweep Type Combobox
    label_sweep_type = customtkinter.CTkLabel(inst_window, text="Sweep Type:")
    label_sweep_type.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    combobox_sweep_type = customtkinter.CTkComboBox(inst_window, values=["Linear Sweep", "Log Sweep"])
    combobox_sweep_type.set("Linear Sweep")
    combobox_sweep_type.grid(row=2, column=1, padx=10, pady=10)

    # Voltage Range
    label_start_voltage = customtkinter.CTkLabel(inst_window, text="Start Voltage (V):")
    label_start_voltage.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_start_voltage = customtkinter.CTkEntry(inst_window)
    entry_start_voltage.grid(row=3, column=1, padx=10, pady=10)

    label_end_voltage = customtkinter.CTkLabel(inst_window, text="End Voltage (V):")
    label_end_voltage.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_end_voltage = customtkinter.CTkEntry(inst_window)
    entry_end_voltage.grid(row=4, column=1, padx=10, pady=10)

    # Step Size
    label_step_size = customtkinter.CTkLabel(inst_window, text="Step Size (V):")
    label_step_size.grid(row=5, column=0, padx=10, pady=10, sticky="e")
    entry_step_size = customtkinter.CTkEntry(inst_window)
    entry_step_size.grid(row=5, column=1, padx=10, pady=10)

    # Limit
    label_limit = customtkinter.CTkLabel(inst_window, text="Limit (A):")
    label_limit.grid(row=6, column=0, padx=10, pady=10, sticky="e")
    entry_limit = customtkinter.CTkEntry(inst_window)
    entry_limit.grid(row=6, column=1, padx=10, pady=10)

    # Measure Combobox
    label_measure = customtkinter.CTkLabel(inst_window, text="Measure:")
    label_measure.grid(row=7, column=0, padx=10, pady=10, sticky="e")
    combobox_measure = customtkinter.CTkComboBox(inst_window, values=["V", "A", "V, A"])
    combobox_measure.set("V, A")
    combobox_measure.grid(row=7, column=1, padx=10, pady=10)

    # Add and Cancel buttons
    def add_instrument():
        name = entry_name.get()
        voltage_type = combobox_voltage_type.get()
        sweep_type = combobox_sweep_type.get()
        start_voltage = entry_start_voltage.get()
        end_voltage = entry_end_voltage.get()
        step_size = entry_step_size.get()
        limit = entry_limit.get()
        measure = combobox_measure.get()

        instrument = {
            'name': name,
            'voltage_type': voltage_type,
            'sweep_type': sweep_type,
            'start_voltage': start_voltage,
            'end_voltage': end_voltage,
            'step_size': step_size,
            'limit': limit,
            'measure': measure
        }
        instruments_list.append(instrument)
        inst_window.destroy()
        update_instrument_list()

    button_add = customtkinter.CTkButton(inst_window, text="Add", command=add_instrument)
    button_add.grid(row=8, column=0, padx=10, pady=20)
    button_cancel = customtkinter.CTkButton(inst_window, text="Cancel", command=inst_window.destroy)
    button_cancel.grid(row=8, column=1, padx=10, pady=20)

    inst_window.grid_columnconfigure(0, weight=1)
    inst_window.grid_columnconfigure(1, weight=1)

button_add_instrument = customtkinter.CTkButton(master=frame_instruments, text="Add Instrument", command=show_panel)
button_add_instrument.pack(pady=10)

# Instruments List
instruments_list = []

# Scrollable Frame to display instruments
scrollable_frame_instruments = customtkinter.CTkScrollableFrame(master=frame_instruments, width=280, height=500)
scrollable_frame_instruments.pack(pady=(0,10), padx=10)

def update_instrument_list():
    # Clear the scrollable_frame
    for widget in scrollable_frame_instruments.winfo_children():
        widget.destroy()

    # Add labels for each instrument
    for idx, instrument in enumerate(instruments_list):
        label_inst = customtkinter.CTkLabel(scrollable_frame_instruments, text=f"{instrument['name']}", font=('Arial', 14, 'bold'))
        label_inst.pack(pady=(10, 0))

        params_text = (
            f"{instrument['voltage_type']}, {instrument['sweep_type']}\n"
            f"{instrument['start_voltage']}V - {instrument['end_voltage']}V\n"
            f"Step: {instrument['step_size']}V\n"
            f"Limit: {instrument['limit']}A\n"
            f"Measure: {instrument['measure']}"
        )
        label_params = customtkinter.CTkLabel(scrollable_frame_instruments, text=params_text)
        label_params.pack(pady=(0, 10))


# ===================================================================
# EXPERIMENTS COLUMN (Next to Instruments)
frame_experiments = customtkinter.CTkFrame(app, width=300, height=700)
frame_experiments.grid(row=0, column=1, sticky="ns", padx=(5, 5), pady=10)

experiment_label = customtkinter.CTkLabel(frame_experiments, text="Experiments", font=('Arial', 16, 'bold'))
experiment_label.pack(pady=(10, 0))

experiments_list = []

def update_experiment_list():
    # Clear the experiment scrollable_frame
    for widget in scrollable_frame_experiments.winfo_children():
        widget.destroy()

    # Add labels for each experiment
    for idx, experiment in enumerate(experiments_list):
        label_exp = customtkinter.CTkLabel(scrollable_frame_experiments, text=f"{experiment['name']}", font=('Arial', 14, 'bold'))
        label_exp.pack(pady=(10, 0))

        params_text = (
            f"Type: {experiment['type']}\n"
            f"Description: {experiment['description']}\n"
            f"Start: {experiment['start_time']}\n"
            f"End: {experiment['end_time']}"
        )
        label_params = customtkinter.CTkLabel(scrollable_frame_experiments, text=params_text)
        label_params.pack(pady=(0, 10))

def show_experiment_panel():
    # Create a Toplevel window for the pop-up
    exp_window = customtkinter.CTkToplevel(app)
    exp_window.geometry("400x500")
    exp_window.title("Add Experiment")

    exp_window.transient(app)
    exp_window.grab_set()
    exp_window.focus_force()

    # Experiment Name
    label_name = customtkinter.CTkLabel(exp_window, text="Experiment Name:")
    label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_name = customtkinter.CTkEntry(exp_window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    # Experiment Type Combobox
    label_type = customtkinter.CTkLabel(exp_window, text="Experiment Type:")
    label_type.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    combobox_type = customtkinter.CTkComboBox(exp_window, values=["Calibration", "Measurement", "Test"])
    combobox_type.set("Calibration")
    combobox_type.grid(row=1, column=1, padx=10, pady=10)

    # Experiment Description
    label_description = customtkinter.CTkLabel(exp_window, text="Description:")
    label_description.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_description = customtkinter.CTkEntry(exp_window, width=300)
    entry_description.grid(row=2, column=1, padx=10, pady=10)

    # Start and End Time
    label_start_time = customtkinter.CTkLabel(exp_window, text="Start Time:")
    label_start_time.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_start_time = customtkinter.CTkEntry(exp_window)
    entry_start_time.grid(row=3, column=1, padx=10, pady=10)

    label_end_time = customtkinter.CTkLabel(exp_window, text="End Time:")
    label_end_time.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_end_time = customtkinter.CTkEntry(exp_window)
    entry_end_time.grid(row=4, column=1, padx=10, pady=10)

    def add_experiment():
        name = entry_name.get()
        exp_type = combobox_type.get()
        description = entry_description.get()
        start_time = entry_start_time.get()
        end_time = entry_end_time.get()

        experiment = {
            'name': name,
            'type': exp_type,
            'description': description,
            'start_time': start_time,
            'end_time': end_time
        }
        experiments_list.append(experiment)
        exp_window.destroy()
        update_experiment_list()

    button_add = customtkinter.CTkButton(exp_window, text="Add", command=add_experiment)
    button_add.grid(row=5, column=0, padx=10, pady=20)
    button_cancel = customtkinter.CTkButton(exp_window, text="Cancel", command=exp_window.destroy)
    button_cancel.grid(row=5, column=1, padx=10, pady=20)

    exp_window.grid_columnconfigure(0, weight=1)
    exp_window.grid_columnconfigure(1, weight=1)

add_experiment_button = customtkinter.CTkButton(master=frame_experiments, text="Add Experiment", command=show_experiment_panel)
add_experiment_button.pack(pady=10)

scrollable_frame_experiments = customtkinter.CTkScrollableFrame(master=frame_experiments, width=280, height=500)
scrollable_frame_experiments.pack(pady=(0,10), padx=10)


# ===================================================================
# RADIOBUTTONS EXAMPLE==============
def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

radio_var = tkinter.IntVar(value=0)
radiobutton_1 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Voltage", command=radiobutton_event, variable=radio_var, value=1)
radiobutton_2 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Current", command=radiobutton_event, variable=radio_var, value=2)

radiobutton_1.grid(row=1, column=2)
radiobutton_2.grid(row=1, column=3)

label = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Type", fg_color="transparent", pady=10)
label.grid(row=1, column=0)

# LABEL EXAMPLE WITH ENTRY==========================
label = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Start", fg_color="transparent", padx=5, pady=10)
label.grid(row=4, column=0)

entry = customtkinter.CTkEntry(master=tabview.tab("Settings"), placeholder_text="")
entry.grid(row=4, column=2)

label = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="V", fg_color="transparent", justify='left', anchor='w', width=80)
label.grid(row=4, column=3)

# LABEL WITH COMBOBOX================================
def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

label = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Mode", fg_color="transparent")
label.grid(row=10, column=0)

combobox = customtkinter.CTkComboBox(master=tabview.tab("Settings"), values=["DC", "Pulse"], command=combobox_callback)
combobox.set("DC")
combobox.grid(row=10, column=2)

# Changing Label================================
labelchg = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="0", fg_color="transparent", pady=10)
labelchg.grid(row=11, column=0)
labelchg.configure(text=time.strftime('%H:%M:%S'))

# Progress Bar=====================
progressbar = customtkinter.CTkProgressBar(master=tabview.tab("Settings"), orientation="horizontal")
progressbar.grid(row=12, column=0)
progressbar.start()

# ==============================
# TABLE TAB
height = 20
width = 10
for i in range(height):  # Rows
    for j in range(width):  # Columns
        b = customtkinter.CTkLabel(master=tabview.tab("Table"), text="0", fg_color='gray20', width=90, height=25)
        b.grid(row=i, column=j, padx=1, pady=1)

app.mainloop()
