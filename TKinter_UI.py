import tkinter
import customtkinter
import time

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window 
app.geometry("1366x768")
app.resizable(False, False)
app.title("Nano - Device Window")
app.grid_rowconfigure(0, weight=1)  # configure grid system to be center alligned
app.grid_columnconfigure(0, weight=1)

def button_function():
    print("button pressed")


tabview = customtkinter.CTkTabview(master=app, width=1000, height=800, anchor='w', corner_radius=10)
tabview.grid(row=0, column=1)

#Tabs
#===========================================
TABsettings = tabview.add("Settings")  
TABtable = tabview.add("Table")
TABgraph = tabview.add("Graph")  
tabview.set("Settings")  # set currently visible tab

#Add Instrument Frame
#===========================================
def show_panel():
    # Create a frame for the popup panel
    inst_frame = customtkinter.CTkFrame(app,  width=300, height=400, border_width = 1)
    inst_frame.place(x=27, y=20)  # Center the panel in the main window

    # Add content to the panel
    inst_label = customtkinter.CTkLabel(inst_frame, text="Available Hardware:", height=100, anchor='n')
    inst_button = customtkinter.CTkButton(inst_frame, text="Close", command=inst_frame.destroy)

    inst_label.grid(row=0, column=0, pady=100, padx=100)
    inst_button.grid(row=1, column=0, padx=5, pady=5)


frame = customtkinter.CTkFrame(app, width=300, height=700)
frame.grid(row=0, column=0)


button = customtkinter.CTkButton(master=app, text="Add Instrument", command=show_panel)
button.place(x=110, y=80)

#entry = customtkinter.CTkEntry(master=tabview.tab("Table"), placeholder_text="CTkEntry")
#entry.grid(row=4, column=0)



#RADIOBUTTONS EXAMPLE==============
def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

#LABEL EXAMPLE with RADIOBUTTON====================
radio_var = tkinter.IntVar(value=0)
radiobutton_1 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Voltage", command=radiobutton_event, variable=radio_var, value=1)
radiobutton_2 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Current", command=radiobutton_event, variable=radio_var, value=2)

radiobutton_1.grid(row=1, column=2)
radiobutton_2.grid(row=1, column=3)

label = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Type", fg_color="transparent", pady=10)
label.grid(row=1, column=0)

#LABEL EXAMPLE WITH ENTRY==========================
label = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Start", fg_color="transparent", padx=5, pady=10)
label.grid(row=4, column=0)

entry = customtkinter.CTkEntry(master=tabview.tab("Settings"), placeholder_text="")
entry.grid(row=4, column=2)

label = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="V", fg_color="transparent", justify='left', anchor='w', width=80)
label.grid(row=4, column=3)

#LABEL WITH COMBOBOX================================
def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

label = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Mode", fg_color="transparent")
label.grid(row=10, column=0)

combobox = customtkinter.CTkComboBox(master=tabview.tab("Settings"), values=["DC", "Pulse"], command=combobox_callback)
combobox.set("DC")
combobox.grid(row=10, column=2)

#Changing Label================================
labelchg = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="0", fg_color="transparent", pady=10)
labelchg.grid(row=11, column=0)
labelchg.configure(text=time)

#Progress Bar=====================
progressbar = customtkinter.CTkProgressBar(master=tabview.tab("Settings"), orientation="horizontal")
progressbar.grid(row=12, column=0)
progressbar.start()

#==============================
#TABLE TAB
height = 20
width = 10
for i in range(height): #Rows
    for j in range(width): #Columns
        b = customtkinter.CTkLabel(master=tabview.tab("Table"), text="0", fg_color='gray20', width=90, height=25)
        b.grid(row=i, column=j, padx=1, pady=1)

app.mainloop()