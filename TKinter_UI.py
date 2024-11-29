import tkinter
import customtkinter
import time

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window 
app.geometry("1366x768")
app.resizable(False, False)
app.title("Nano - Device Window")
app.grid_rowconfigure(0, weight=1)  # configure grid system to be center aligned
app.grid_columnconfigure(0, weight=1)

# Instruments List
instruments_list = []

# Variable to keep track of the current instrument index
current_instrument_index = None

# Left Frame
frame = customtkinter.CTkFrame(app, width=300, height=700)
frame.grid(row=0, column=0)

# Scrollable Frame to display instruments
scrollable_frame = customtkinter.CTkScrollableFrame(master=frame, width=280, height=600)
scrollable_frame.pack(pady=20, padx=10)

# Main Tabview (Will contain instrument-specific tabs)
main_tabview = None  # We'll initialize this in the initialize_main_tabview function

# Function to update instrument list display
def update_instrument_list():
    # Clear the scrollable_frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Add labels for each instrument
    for idx, instrument in enumerate(instruments_list):
        # Instrument Button
        button_inst = customtkinter.CTkButton(scrollable_frame, text=f"{instrument['name']}", command=lambda idx=idx: select_instrument(idx))
        button_inst.pack(pady=(10, 0))

        # Display parameters
        params_text = (
            f"{instrument['voltage_type']}, {instrument['sweep_type']}\n"
            f"Start: {instrument['start']}V, Stop: {instrument['stop']}V\n"
            f"Step: {instrument['step_size']}V\n"
            f"Limit: {instrument['limit']}A, Bias Level: {instrument['bias_level']}V\n"
            f"Measure: {instrument['measure']}"
        )
        label_params = customtkinter.CTkLabel(scrollable_frame, text=params_text)
        label_params.pack(pady=(0, 10))

# Function to select an instrument
def select_instrument(index):
    global current_instrument_index
    current_instrument_index = index
    update_tabs_for_instrument()

# Function to update the tabs for the selected instrument
def update_tabs_for_instrument():
    global main_tabview

    # Destroy the existing tabview if it exists
    if main_tabview is not None:
        main_tabview.destroy()

    # Recreate the tabview
    main_tabview = customtkinter.CTkTabview(master=app, width=1000, height=800, corner_radius=10)
    main_tabview.grid(row=0, column=1)

    # Get the current instrument
    instrument = instruments_list[current_instrument_index]

    # Add tabs
    tab_settings = main_tabview.add("Settings")
    tab_table = main_tabview.add("Table")
    tab_graph = main_tabview.add("Graph")
    main_tabview.set("Settings")

    # Update the Settings tab
    update_settings_tab(tab_settings, instrument)

    # Update the Table tab
    update_table_tab(tab_table, instrument)

    # Update the Graph tab (Placeholder)
    update_graph_tab(tab_graph, instrument)

# Function to update the Settings tab
def update_settings_tab(tab, instrument):
    # Variables to hold entry values
    name_var = tkinter.StringVar(value=instrument['name'])
    start_var = tkinter.StringVar(value=instrument['start'])
    stop_var = tkinter.StringVar(value=instrument['stop'])
    limit_var = tkinter.StringVar(value=instrument['limit'])
    bias_level_var = tkinter.StringVar(value=instrument['bias_level'])
    step_size_var = tkinter.StringVar(value=instrument['step_size'])
    measure_var = tkinter.StringVar(value=instrument['measure'])
    voltage_type_var = tkinter.StringVar(value=instrument['voltage_type'])
    sweep_type_var = tkinter.StringVar(value=instrument['sweep_type'])

    # Labels and Entry widgets
    # Instrument Name
    label_name = customtkinter.CTkLabel(tab, text="Instrument Name:")
    label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_name = customtkinter.CTkEntry(tab, textvariable=name_var)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    # Start Voltage
    label_start = customtkinter.CTkLabel(tab, text="Start (V):")
    label_start.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_start = customtkinter.CTkEntry(tab, textvariable=start_var)
    entry_start.grid(row=1, column=1, padx=10, pady=10)

    # Stop Voltage
    label_stop = customtkinter.CTkLabel(tab, text="Stop (V):")
    label_stop.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_stop = customtkinter.CTkEntry(tab, textvariable=stop_var)
    entry_stop.grid(row=2, column=1, padx=10, pady=10)

    # Limit
    label_limit = customtkinter.CTkLabel(tab, text="Limit (A):")
    label_limit.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_limit = customtkinter.CTkEntry(tab, textvariable=limit_var)
    entry_limit.grid(row=3, column=1, padx=10, pady=10)

    # Bias Level
    label_bias = customtkinter.CTkLabel(tab, text="Bias Level (V):")
    label_bias.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_bias = customtkinter.CTkEntry(tab, textvariable=bias_level_var)
    entry_bias.grid(row=4, column=1, padx=10, pady=10)

    # Step Size
    label_step = customtkinter.CTkLabel(tab, text="Step Size (V):")
    label_step.grid(row=5, column=0, padx=10, pady=10, sticky="e")
    entry_step = customtkinter.CTkEntry(tab, textvariable=step_size_var)
    entry_step.grid(row=5, column=1, padx=10, pady=10)

    # Measure
    label_measure = customtkinter.CTkLabel(tab, text="Measure:")
    label_measure.grid(row=6, column=0, padx=10, pady=10, sticky="e")
    combobox_measure = customtkinter.CTkComboBox(tab, values=["V", "A", "V, A"], variable=measure_var)
    combobox_measure.grid(row=6, column=1, padx=10, pady=10)

    # Voltage Type
    label_voltage_type = customtkinter.CTkLabel(tab, text="Voltage Type:")
    label_voltage_type.grid(row=7, column=0, padx=10, pady=10, sticky="e")
    combobox_voltage_type = customtkinter.CTkComboBox(tab, values=["DC Voltage", "AC Voltage"], variable=voltage_type_var)
    combobox_voltage_type.grid(row=7, column=1, padx=10, pady=10)

    # Sweep Type
    label_sweep_type = customtkinter.CTkLabel(tab, text="Sweep Type:")
    label_sweep_type.grid(row=8, column=0, padx=10, pady=10, sticky="e")
    combobox_sweep_type = customtkinter.CTkComboBox(tab, values=["Linear Sweep", "Log Sweep"], variable=sweep_type_var)
    combobox_sweep_type.grid(row=8, column=1, padx=10, pady=10)

    # Radio Buttons
    def radiobutton_event():
        print("Radiobutton toggled, current value:", radio_var.get())

    radio_var = tkinter.IntVar(value=0)
    radiobutton_1 = customtkinter.CTkRadioButton(master=tab, text="Voltage", command=radiobutton_event, variable=radio_var, value=1)
    radiobutton_2 = customtkinter.CTkRadioButton(master=tab, text="Current", command=radiobutton_event, variable=radio_var, value=2)
    radiobutton_1.grid(row=9, column=0, padx=10, pady=10)
    radiobutton_2.grid(row=9, column=1, padx=10, pady=10)

    # Combobox Example
    def combobox_callback(choice):
        print("Combobox dropdown clicked:", choice)

    label_mode = customtkinter.CTkLabel(master=tab, text="Mode:")
    label_mode.grid(row=10, column=0, padx=10, pady=10, sticky="e")
    combobox_mode = customtkinter.CTkComboBox(master=tab, values=["DC", "Pulse"], command=combobox_callback)
    combobox_mode.set("DC")
    combobox_mode.grid(row=10, column=1, padx=10, pady=10)

    # Changing Label (Display Current Time)
    label_time = customtkinter.CTkLabel(master=tab, text="", fg_color="transparent", pady=10)
    label_time.grid(row=11, column=0, columnspan=2)

    def update_time():
        current_time = time.strftime('%H:%M:%S')
        label_time.configure(text=f"Current Time: {current_time}")
        tab.after(1000, update_time)  # Update every second

    update_time()  # Start the time update loop

    # Progress Bar
    progressbar = customtkinter.CTkProgressBar(master=tab, orientation="horizontal")
    progressbar.grid(row=12, column=0, columnspan=2, padx=10, pady=10)
    progressbar.set(0.5)  # Set to 50% for demonstration

    # Save Button
    def save_instrument_settings():
        # Update the instrument data
        instrument['name'] = name_var.get()
        instrument['start'] = start_var.get()
        instrument['stop'] = stop_var.get()
        instrument['limit'] = limit_var.get()
        instrument['bias_level'] = bias_level_var.get()
        instrument['step_size'] = step_size_var.get()
        instrument['measure'] = measure_var.get()
        instrument['voltage_type'] = voltage_type_var.get()
        instrument['sweep_type'] = sweep_type_var.get()

        # Update the instrument list display
        update_instrument_list()

    button_save = customtkinter.CTkButton(tab, text="Save", command=save_instrument_settings)
    button_save.grid(row=13, column=0, columnspan=2, pady=20)

    # Adjust column weights to improve layout
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_columnconfigure(1, weight=1)

# Function to update the Table tab
def update_table_tab(tab, instrument):
    # Clear the tab
    for widget in tab.winfo_children():
        widget.destroy()

    # TABLE TAB
    height = 20
    width = 10
    for i in range(height):  # Rows
        for j in range(width):  # Columns
            b = customtkinter.CTkLabel(master=tab, text="0", fg_color='gray20', width=90, height=25)
            b.grid(row=i, column=j, padx=1, pady=1)

# Function to update the Graph tab (Placeholder)
def update_graph_tab(tab, instrument):
    # Clear the tab
    for widget in tab.winfo_children():
        widget.destroy()

    # For demonstration purposes, we'll just display a placeholder graph
    label = customtkinter.CTkLabel(tab, text=f"Graph for {instrument['name']}")
    label.pack(pady=20)

# Function to show the Add Instrument panel
def show_panel():
    # Create a Toplevel window for the pop-up
    inst_window = customtkinter.CTkToplevel(app)
    inst_window.geometry("400x6 00")
    inst_window.title("Add Instrument")

    # Bring the window to the front
    inst_window.transient(app)  # Set to be on top of main window
    inst_window.grab_set()      # Make the popup modal
    inst_window.focus_force()   # Focus on the popup

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

    # Start Voltage
    label_start = customtkinter.CTkLabel(inst_window, text="Start (V):")
    label_start.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_start = customtkinter.CTkEntry(inst_window)
    entry_start.grid(row=3, column=1, padx=10, pady=10)

    # Stop Voltage
    label_stop = customtkinter.CTkLabel(inst_window, text="Stop (V):")
    label_stop.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_stop = customtkinter.CTkEntry(inst_window)
    entry_stop.grid(row=4, column=1, padx=10, pady=10)

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

    # Bias Level
    label_bias_level = customtkinter.CTkLabel(inst_window, text="Bias Level (V):")
    label_bias_level.grid(row=7, column=0, padx=10, pady=10, sticky="e")
    entry_bias_level = customtkinter.CTkEntry(inst_window)
    entry_bias_level.grid(row=7, column=1, padx=10, pady=10)

    # Measure Combobox
    label_measure = customtkinter.CTkLabel(inst_window, text="Measure:")
    label_measure.grid(row=8, column=0, padx=10, pady=10, sticky="e")
    combobox_measure = customtkinter.CTkComboBox(inst_window, values=["V", "A", "V, A"])
    combobox_measure.set("V, A")
    combobox_measure.grid(row=8, column=1, padx=10, pady=10)

    # Add and Cancel buttons
    def add_instrument():
        # Get the values from the entries
        name = entry_name.get()
        voltage_type = combobox_voltage_type.get()
        sweep_type = combobox_sweep_type.get()
        start = entry_start.get()
        stop = entry_stop.get()
        step_size = entry_step_size.get()
        limit = entry_limit.get()
        bias_level = entry_bias_level.get()
        measure = combobox_measure.get()

        # Store the instrument data
        instrument = {
            'name': name,
            'voltage_type': voltage_type,
            'sweep_type': sweep_type,
            'start': start,
            'stop': stop,
            'step_size': step_size,
            'limit': limit,
            'bias_level': bias_level,
            'measure': measure
        }
        instruments_list.append(instrument)

        # Close the window
        inst_window.destroy()

        # Update the GUI to show the added instruments
        update_instrument_list()

        # Set the current instrument and update tabs
        global current_instrument_index
        current_instrument_index = len(instruments_list) - 1
        update_tabs_for_instrument()

    button_add = customtkinter.CTkButton(inst_window, text="Add", command=add_instrument)
    button_add.grid(row=9, column=0, padx=10, pady=20)
    button_cancel = customtkinter.CTkButton(inst_window, text="Cancel", command=inst_window.destroy)
    button_cancel.grid(row=9, column=1, padx=10, pady=20)

    # Adjust column weights to improve layout
    inst_window.grid_columnconfigure(0, weight=1)
    inst_window.grid_columnconfigure(1, weight=1)

# "Add Instrument" Button
button = customtkinter.CTkButton(master=app, text="Add Instrument", command=show_panel)
button.place(x=110, y=80)

# Initialize the main_tabview with a default message
def initialize_main_tabview():
    global main_tabview

    # Destroy the existing tabview if it exists
    if main_tabview is not None:
        main_tabview.destroy()

    # Create a new tabview
    main_tabview = customtkinter.CTkTabview(master=app, width=1000, height=800, corner_radius=10)
    main_tabview.grid(row=0, column=1)

    # Add a default tab
    tab_default = main_tabview.add("Welcome")
    label_default = customtkinter.CTkLabel(tab_default, text="Please add an instrument or select one from the list.")
    label_default.pack(pady=20)

initialize_main_tabview()

app.mainloop()
