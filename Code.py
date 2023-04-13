from zaber_motion import Units, Library
from zaber_motion.ascii import Connection, SettingConstants
from zaber_motion.ascii import AlertEvent
from zaber_motion.ascii import Axis
from zaber_motion.gcode import axis_definition
from tkinter import *
from tkinter import ttk
#from zaber_motion import Units, Library
#from zaber_motion.ascii import Connection, SettingConstants
from zaber_motion import ConnectionFailedException

import tkinter.filedialog as filedialog
import tkinter as tk
import subprocess
import zaber_motion
import serial.tools.list_ports as list_ports



class PortSelection:
    def __init__(self, master):
        self.master = master
        master.title("Selecting the COM port")

        self.label = tk.Label(master, text="Enter the COM port number:")
        self.label.pack()

        self.com_entry = tk.Entry(master)
        self.com_entry.pack()

        self.error_label = tk.Label(master, text="", fg="red")
        self.error_label.pack()

        self.validate_button = tk.Button(master, text="Validate", command=self.validate_port)
        self.validate_button.pack()

    def validate_port(self):
        com_port = self.com_entry.get()
        if not com_port.startswith("COM"):
            self.error_label.config(text="The port number must start with COM")
            return
    
        available_ports = [p.device for p in list_ports.comports()]
        if com_port not in available_ports:
            self.error_label.config(text="The port {} is not available".format(com_port))
            return
    
        self.master.withdraw()
        interface = Interface(com_port)
        interface.master.deiconify()
        
class Interface:
    
    #axis.settings.get("encoder.pos")
    
    def __init__(self, master):
        self.LSQ1 = NONE
        self.LSQ2 = NONE
        self.master = master
        master.title("My window")
        self.device_list = []
        
        self.num_devices = tk.IntVar()
        self.num_COM = tk.StringVar()
        self.file_path = tk.StringVar()
        self.file_name = tk.StringVar()
        self.number150 = tk.DoubleVar()
        self.number50 = tk.DoubleVar()
        self.device = None

       
        
        # First part the number com and the connection button
        tk.Label(master, text="COM NUMBER :").grid(row=0, column=0)
        self.connect_button = ttk.Button(master, text="Connection", command=self.connection)
        self.connect_button.grid(column=5, row=0)
        self.path_text = tk.Entry(self.master, textvariable=self.num_COM, width=30)
        self.path_text.grid(row=0, column=1, sticky="W", padx=5, columnspan=4)
        self.disconnect_button = ttk.Button(master, text="Deconnection", command=self.deconnection)
        self.disconnect_button.grid(column=6, row=0)
        
        # Second part the number devices found
        
        tk.Label(master, text="Found : ").grid(row=1, column=0)
        tk.Label(master, text="devices").grid(row=1, column=2)
        self.file_number = "text.txt"
        number_label = tk.Label(self.master, textvariable=self.num_devices).grid(row=1, column=1)

        
        # Third part the position
        tk.Label(master, text="").grid(row=2, column=1)
        tk.Label(master, text="Position").grid(row=3, column=1)


        # Fourth part the 150 mm engine
        
        tk.Label(master, text="Motorized linear stage 150mm ").grid(row=4, column=0)
        tk.Label(master, textvariable=self.number150).grid(row=4, column=1)
        tk.Label(master, text="mm").grid(row=4, column=2)
       
        self.r3=ttk.Button(master, text="►", width=10).grid(column=7, row=4)
        self.r4=ttk.Button(master, text="►►", width=10).grid(column=8, row=4)
        self.r5=ttk.Button(master, text="◄", width=10).grid(column=5, row=4)
        self.r6=ttk.Button(master, text="◄◄", width=10).grid(column=4, row=4)       
        self.r7=ttk.Button(master, text="Home", width=10).grid(column=9, row=4)  
        self.r8=ttk.Button(master, text="█", width=10).grid(column=6, row=4)  


        # Fifth part the 50 mm engine
        
        tk.Label(master, text="Motorized linear stage 50mm ").grid(row=5, column=0)
        tk.Label(master, textvariable=self.number50).grid(row=5, column=1)
        tk.Label(master, text="mm").grid(row=5, column=2)
        # exemple de bouton ttk.Button(frm, text="►", command=root.destroy).grid(column=1, row=3)
        self.r9=ttk.Button(master, text="►", width=10).grid(column=7, row=5)
        self.r10=ttk.Button(master, text="►►", command=self.mouvement, width=10).grid(column=8, row=5)
        self.r11=ttk.Button(master, text="◄", width=10).grid(column=5, row=5)
        self.r12=ttk.Button(master, text="◄◄", width=10).grid(column=4, row=5)       
        self.r13=ttk.Button(master, text="Home", width=10).grid(column=9, row=5)  
        self.r14=ttk.Button(master, text="█", width=10).grid(column=6, row=5) 
        


        # Sixth part the modification of the two engines
        
        tk.Label(master, text="").grid(column=10)
        tk.Label(master, text="").grid(row=6)
        frame = tk.Frame(self.master, width=50, height=50, highlightbackground="black", highlightthickness=2)
        frame.grid(row=0, column=11, rowspan=7)
        self.r15 = ttk.Button(frame, text="HOME", width=10).grid(column=0, row=0)
        self.r16 = ttk.Button(frame, text="█", command=self.stop_all_axes, width=10).grid(column=0, row=1)
        tk.Label(frame, text="").grid(column=1, row= 0)
        tk.Label(frame, text="Move to absolute position").grid(row=0, column=3)
        self.number_text = ttk.Entry(frame, width=30).grid(row=1, column=3, sticky="W", padx=5)
        self.r17=ttk.Button(frame, text="►", width=10).grid(column=5, row=1)
        tk.Label(frame, text="mm").grid(row=1, column=4)

        tk.Label(frame, text="").grid(row=2)
        tk.Label(frame, text="Move by relative position").grid(row=4, column=3)
        self.number_text = ttk.Entry(frame, width=30).grid(row=5, column=3, sticky="W", padx=5)
        self.r18=ttk.Button(frame, text="►", width=10).grid(column=5, row=5)
        self.r19=ttk.Button(frame, text="◄", width=10).grid(column=2, row=5)
        tk.Label(frame, text="mm").grid(row=5, column=4)

        tk.Label(frame, text="").grid(row=6)
        tk.Label(frame, text="Move at velocity").grid(row=7, column=3)
        self.number_text = ttk.Entry(frame, width=30).grid(row=8, column=3, sticky="W", padx=5)
        self.r18=ttk.Button(frame, text="►", width=10).grid(column=5, row=8)
        self.r19=ttk.Button(frame, text="◄", width=10).grid(column=2, row=8)
        tk.Label(frame, text="mm").grid(row=8, column=4)       

        tk.Label(master, text="").grid(row=7)
        frame = tk.Frame(master, height=2, bg='black').grid(row=8, columnspan=15, pady=10, sticky='we')
        tk.Label(master, text="").grid(row=9)



    def connection(self):
        number_COM = "COM" + str(self.num_COM.get())
        self.error_label = None
        try:
            with Connection.open_serial_port(str(number_COM)) as connection:
                self.connection = connection
                devices = connection.detect_devices()
                num_devices = len(devices)
                self.num_devices.set(num_devices)
                device_list = connection.detect_devices()
                print("Found {} devices".format(num_devices))
                for device in device_list:
                    if device.name.startswith("LSQ"):
                        if self.LSQ1 is None:
                            self.LSQ1 = device
                        elif self.LSQ2 is None:
                            self.LSQ2 = device     
        except ConnectionFailedException as ex:
            print(f"Connection error: {ex}")
            if self.error_label:
                self.error_label.configure(text=str(ex))

    def mouvement(self):
        if self.LSQ1 is None:
            print("LSQ1 is not connected")
            return
        obj = eval("self.LSQ1")
        obj.move_absolute(10, Units.LENGTH_MILLIMETRES)
                

    def deconnection(self):
        self.connection.close()
        self.connected = False
        self.LSQ1 = None
        self.LSQ2 = None
        self.LSQ3 = None
        self.LSQ4 = None
        self.LSQ5 = None
        self.LSQ6 = None
        self.devices = None
        num_devices=0
        self.num_devices.set(num_devices)
        print("Found {} devices".format(num_devices))

    def stop_all_axes(self):
        try:
            self.LSQ1.stop()
            self.LSQ2.stop()
        except AttributeError:
            # Axe non initialisé
            pass

    def distance_axe(self):
            position = axis.settings.get("encoder.pos")







# Démarrage de la boucle principale
root = tk.Tk()
interface = Interface(root)
interface.connection()

root.mainloop()