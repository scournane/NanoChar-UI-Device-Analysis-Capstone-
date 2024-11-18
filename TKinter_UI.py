import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

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
TABsettings = tabview.add("Settings")  # add tab at the end
TABtable = tabview.add("Table")  # add tab at the end
TABgraph = tabview.add("Graph")  # add tab at the end
tabview.set("Settings")  # set currently visible tab

#Add Instrument Frame
#===========================================
def show_panel():
    # Create a frame for the popup panel
    popup_frame = customtkinter.CTkFrame(app,  width=500, height=400, border_width = 200)
    popup_frame.place(anchor="nw")  # Center the panel in the main window

    # Add content to the panel
    lbl = customtkinter.CTkLabel(popup_frame, text="Available Hardware:", height=100, anchor='n', pady=200, padx=200)
    btn = customtkinter.CTkButton(popup_frame, text="Close", command=popup_frame.destroy)

    lbl.grid(row=0, column=0)
    btn.grid(row=1, column=0)


frame = customtkinter.CTkFrame(app, width=300, height=700)
frame.grid(row=0, column=0)


button = customtkinter.CTkButton(master=app, text="Add Instrument", command=show_panel)
button.place(x=110, y=80)

entry = customtkinter.CTkEntry(master=tabview.tab("Table"), placeholder_text="CTkEntry")
entry.grid(row=4, column=0)



#RADIOBUTTONS EXAMPLE==============
def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

#LABEL EXAMPLE with RADIOBUTTON====================
radio_var = tkinter.IntVar(value=0)
radiobutton_1 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Voltage", command=radiobutton_event, variable=radio_var, value=1)
radiobutton_2 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Current", command=radiobutton_event, variable=radio_var, value=2)

#radiobutton_1.pack(padx=20, pady=5)
#radiobutton_2.pack(padx=20, pady=5)
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







# Use CTkButton instead of tkinter Button
#button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
#button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

app.mainloop()