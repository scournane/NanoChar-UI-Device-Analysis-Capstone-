import tkinter
import customtkinter
import time
from PIL import Image, ImageTk  #Using Pillow for image manipulation

#Helper Functions
#=========================================
def scale_image(filepath, scale_factor):
    # Open the image using Pillow
    image = Image.open(filepath)
    
    # Calculate the new size (reduce size by the scale factor)
    new_width = int(image.width // scale_factor)
    new_height = int(image.height // scale_factor)
    
    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image


#TKinter Setup
#=========================================
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

#Assets
#===========================================
arrowImg = scale_image('UIAssets/right_arrow.png', 10)
arrowImg  = customtkinter.CTkImage(light_image=arrowImg, size=(30, 30))
horizontalBar = scale_image('UIAssets/horizontal_bar.png', 0.5)
horizontalBar = customtkinter.CTkImage(light_image=horizontalBar, size=(600, 1))

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
    inst_label = customtkinter.CTkLabel(inst_frame, text="Available Hardware", height=200, anchor='n')
    inst_button = customtkinter.CTkButton(inst_frame, text="Close", command=inst_frame.destroy)

    inst_label.grid(row=0, column=0, pady=20, padx=100)
    inst_button.grid(row=1, column=0, padx=5, pady=5)

    add_instrument(inst_frame)

#probably make into a class in the future
def add_instrument(panel):
    inst_panel = customtkinter.CTkFrame(panel,  width=300, height=80, border_width = 1)
    inst_panel.place(x=45, y=60)

    inst_name = customtkinter.CTkLabel(inst_panel, text="Kiethley2450", height=30)
    inst_name.grid(row=0, column=0, pady=10, padx=70)

    #Make an invible button on top of our arrow
    invisible_button = tkinter.Button(inst_panel, text="", bg=inst_name["bg"], activebackground=inst_name["bg"], relief="flat", command=button_function, width=10, height=10)
    invisible_button.place(x=170, y=5)

    #make arrow
    inst_arrow = customtkinter.CTkLabel(inst_panel, text='', image=arrowImg, width=20, height=20)
    inst_arrow.place(x=180, y=10)
    


frame = customtkinter.CTkFrame(app, width=300, height=700)
frame.grid(row=0, column=0)


button = customtkinter.CTkButton(master=app, text="Add Instrument", command=show_panel)
button.place(x=110, y=80)

#entry = customtkinter.CTkEntry(master=tabview.tab("Table"), placeholder_text="CTkEntry")
#entry.grid(row=4, column=0)



#RADIOBUTTONS EXAMPLE==============
def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

#LABEL AND HORIZ. LINE EXAMPLE====================
Source = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Source", fg_color="transparent", pady=10, font=("Arial", 20, "bold"))
Source.grid(row=3, column=0)

#horBar1 = customtkinter.CTkLabel(master=tabview.tab("Settings"), text='', image=horizontalBar, width=10, height=3)
#horBar1.grid(row=1, column=0)

#LABEL EXAMPLE with RADIOBUTTON====================
radio_var = tkinter.IntVar(value=1)
radiobutton_1 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Voltage", command=radiobutton_event, variable=radio_var, value=1)
radiobutton_2 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Current", command=radiobutton_event, variable=radio_var, value=2)
radiobutton_1.grid(row=2, column=1)
radiobutton_2.grid(row=2, column=2)
Function = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Function", fg_color="transparent", pady=20)
Function.grid(row=2, column=0)

radio_var2 = tkinter.IntVar(value=1)
FuncRadio_1 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="DC", command=radiobutton_event, variable=radio_var2, value=1)
FuncRadio_2 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Pulse", command=radiobutton_event, variable=radio_var2, value=2)
FuncRadio_1.grid(row=2, column=7)
FuncRadio_2.grid(row=2, column=8)
Type = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Type", fg_color="transparent", pady=20)
Type.grid(row=2, column=6)

#LABEL EXAMPLE WITH ENTRY==========================
start = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Start", fg_color="transparent", padx=40, pady=10)
start.grid(row=10, column=6)
startEntry = customtkinter.CTkEntry(master=tabview.tab("Settings"), placeholder_text="")
startEntry.grid(row=10, column=7)
Volts1 = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="V", fg_color="transparent", justify='left', anchor='w', width=80)
Volts1.grid(row=10, column=8)

stop = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Stop", fg_color="transparent", padx=40, pady=10)
stop.grid(row=11, column=6)
stopEntry = customtkinter.CTkEntry(master=tabview.tab("Settings"), placeholder_text="")
stopEntry.grid(row=11, column=7)
Volts2 = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="V", fg_color="transparent", justify='left', anchor='w', width=80)
Volts2.grid(row=11, column=8)

Step = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Step", fg_color="transparent", pady=20)
Step.grid(row=12, column=6)
Stepnum = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="10.101 mV", fg_color="transparent", pady=20)
Stepnum.grid(row=12, column=7)

#LABEL WITH COMBOBOX================================
def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

Mode = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Mode", fg_color="transparent")
Mode.grid(row=10, column=0)

combobox1 = customtkinter.CTkComboBox(master=tabview.tab("Settings"), values=["DC", "Pulse"], command=combobox_callback)
combobox1.set("DC")
combobox1.grid(row=10, column=1)

check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(master=tabview.tab("Settings"), text="Dual Sweep", command=combobox_callback, variable=check_var, onvalue="on", offvalue="off")
checkbox.grid(row=11, column=0)

Range = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Range", fg_color="transparent")
Range.grid(row=12, column=0)

combobox2 = customtkinter.CTkComboBox(master=tabview.tab("Settings"), values=["Auto", "Manual"], command=combobox_callback)
combobox2.set("Auto")
combobox2.grid(row=12, column=1)

Limit = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Limit", fg_color="transparent")
Limit.grid(row=13, column=0)

combobox3 = customtkinter.CTkComboBox(master=tabview.tab("Settings"), values=["1E-05 A", "05-10 A"], command=combobox_callback)
combobox3.set("1E-05 A")
combobox3.grid(row=13, column=1)

Measure = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Measure", fg_color="transparent", pady=15, font=("Arial", 20, "bold"))
Measure.grid(row=15, column=0)

check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(master=tabview.tab("Settings"), text="Voltage", command=combobox_callback, height=30, variable=check_var, onvalue="on", offvalue="off")
checkbox.grid(row=16, column=0)
check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(master=tabview.tab("Settings"), text="Current", command=combobox_callback, height=30, variable=check_var, onvalue="on", offvalue="off")
checkbox.grid(row=17, column=0)
check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(master=tabview.tab("Settings"), text="Power", command=combobox_callback, height=30, variable=check_var, onvalue="on", offvalue="off")
checkbox.grid(row=18, column=0)
check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(master=tabview.tab("Settings"), text="Resistance", command=combobox_callback, height=30, variable=check_var, onvalue="on", offvalue="off")
checkbox.grid(row=19, column=0)

MinimumRange = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Minimum Range", fg_color="transparent", pady=5)
MinimumRange.grid(row=16, column=6)

combobox3 = customtkinter.CTkComboBox(master=tabview.tab("Settings"), values=["5 mA", "10 mA", "20 mA"], command=combobox_callback)
combobox3.set("5 mA")
combobox3.grid(row=16, column=7)

AutoZero = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Auto Zero", fg_color="transparent", pady=5)
AutoZero.grid(row=17, column=6)

combobox4 = customtkinter.CTkComboBox(master=tabview.tab("Settings"), values=["On", "Off"], command=combobox_callback)
combobox4.set("On")
combobox4.grid(row=17, column=7)

InstrumentSettings = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Instrument Settings", fg_color="transparent", pady=15, font=("Arial", 20, "bold"))
InstrumentSettings.grid(row=25, column=0)

radio_var3 = tkinter.IntVar(value=1)
FuncRadio_3 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Front", command=radiobutton_event, variable=radio_var3, value=1)
FuncRadio_4 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Rear", command=radiobutton_event, variable=radio_var3, value=2)
FuncRadio_3.grid(row=26, column=1)
FuncRadio_4.grid(row=26, column=2)
InputTerminals = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Input Terminals", fg_color="transparent", pady=10)
InputTerminals.grid(row=26, column=0)

radio_var4 = tkinter.IntVar(value=1)
FuncRadio_5 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="2-Wire", command=radiobutton_event, variable=radio_var4, value=1)
FuncRadio_6 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="4-Wire", command=radiobutton_event, variable=radio_var4, value=2)
FuncRadio_5.grid(row=27, column=1)
FuncRadio_6.grid(row=27, column=2)
Sense = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Sense", fg_color="transparent", pady=10)
Sense.grid(row=27, column=0)

HighCapacitanceval = customtkinter.StringVar(value="on")
HighCapacitance = customtkinter.CTkCheckBox(master=tabview.tab("Settings"), text="High Capacitance", command=combobox_callback, variable=HighCapacitanceval, onvalue="on", offvalue="off")
HighCapacitance.grid(row=26, column=7)

outputOff = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="Output Off", fg_color="transparent", padx=40, pady=10)
outputOff.grid(row=27, column=6)
combobox5 = customtkinter.CTkComboBox(master=tabview.tab("Settings"), values=["Normal", "Limited", "Off"], command=combobox_callback)
combobox5.set("Normal")
combobox5.grid(row=27, column=7)

#Changing Label================================
#labelchg = customtkinter.CTkLabel(master=tabview.tab("Settings"), text="0", fg_color="transparent", pady=10)
#labelchg.grid(row=15, column=0)
#labelchg.configure(text=time)

#Progress Bar=====================
#progressbar = customtkinter.CTkProgressBar(master=tabview.tab("Settings"), orientation="horizontal")
#progressbar.grid(row=16, column=0)
#progressbar.start()

#==============================
#TABLE TAB
height = 20
width = 10
for i in range(height): #Rows
    for j in range(width): #Columns
        b = customtkinter.CTkLabel(master=tabview.tab("Table"), text="0", fg_color='gray20', width=90, height=25)
        b.grid(row=i, column=j, padx=1, pady=1)

app.mainloop()