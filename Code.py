# You have to download since the "Python\Python311\Lib\site-packages" many
# different libraries named : zaber, zaber.serial-0.9.1.dist-info, zaber_motion,
# zaber_motion_bindings_windows, zaber_motion_bindings_windows-3.1.1.dist-info,
# zaber_motion-3.1.1.dist-info, tkinter, time, serial.tools.list_ports, serial.
# You can also take this library since another computer and paste it in the
# "site-packages" file.

import tkinter.filedialog as filedialog
import tkinter as tk
import subprocess
import zaber_motion
import serial.tools.list_ports as list_ports
import time
import random


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


with Connection.open_serial_port("COM8") as connection:
    connection.enable_alerts()
    
    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))



    device = device_list[0]
    axis1 = device.get_axis(1)
    axis2 = device.get_axis(2)

    
    class Interface:
        
        
        #axis.settings.get("encoder.pos")
        
        def __init__(self, master):
            self.LSQ1 = NONE
            self.LSQ2 = NONE
            self.master = master
            master.title("My window")
            self.device_list = []
            #axis1.limit.max=10
            
            self.num_devices = tk.IntVar()
            self.num_COM = tk.StringVar()
            self.file_path = tk.StringVar()
            self.file_name = tk.StringVar()
            self.device = None
            
            self.number50_str = tk.StringVar(value="")
            self.number150_str = tk.StringVar(value="")
            
            self.number150_str = tk.StringVar(value=str(axis1.get_position(Units.LENGTH_MILLIMETRES)))
            self.number50_str = tk.StringVar(value=str(axis2.get_position(Units.LENGTH_MILLIMETRES)))
            
            axis1.settings.set("limit.max", 140, Units.LENGTH_MILLIMETRES)
            axis2.settings.set("limit.max", 45, Units.LENGTH_MILLIMETRES)
    
            print(f"\nPosition axe 1 : {self.number150_str.get()}")
            print(f"\nPosition axe 2 : {self.number50_str.get()}")
    
    
            # First part the number com and the connection button
            tk.Label(master, text="COM NUMBER :").grid(row=0, column=0)
            #self.connect_button = ttk.Button(master, text="Connection")
            #self.connect_button.grid(column=5, row=0)
            self.path_text = tk.Label(master, text="COM8", width=5)
            self.path_text.grid(row=0, column=1, sticky="W", padx=5, columnspan=4)
            self.disconnect_button = ttk.Button(master, text="Deconnection")
            self.disconnect_button.grid(column=6, row=0)
            
            # Second part the number devices found
            
            tk.Label(master, text="Found : ").grid(row=1, column=0)
            tk.Label(master, text="devices").grid(row=1, column=2)
            self.file_number = "text.txt"
            self.device_list = device_list
            self.number_label = tk.Label(master, text=" {} ".format(len(self.device_list)))
        
            self.number_label.grid(row=1, column=1)
            
            # Third part the position
            tk.Label(master, text="").grid(row=2, column=1)
            tk.Label(master, text="Position").grid(row=3, column=1)
    
    
            # Fourth part the 150 mm engine
            
            tk.Label(master, text="Motorized linear stage 150mm, Axis 1 ").grid(row=4, column=0)
            tk.Label(master, textvariable=self.number150_str).grid(row=4, column=1)
            tk.Label(master, text="mm").grid(row=4, column=2)
           
            self.r3=ttk.Button(master, text="►",command=lambda:self.increase(1), width=10).grid(column=7, row=4)
            self.r4=ttk.Button(master, text="►►", width=10).grid(column=8, row=4)
            self.r5=ttk.Button(master, text="◄", width=10).grid(column=5, row=4)
            self.r6=ttk.Button(master, text="◄◄", width=10).grid(column=4, row=4)       
            self.r7=ttk.Button(master, text="Home", width=10).grid(column=9, row=4)  
            self.r8=ttk.Button(master, text="█", width=10, command=self.stop_all_axes()).grid(column=6, row=4)  
    
    
            # Fifth part the 50 mm engine
            
            tk.Label(master, text="Motorized linear stage 50mm, Axis 2").grid(row=5, column=0)
            tk.Label(master, textvariable=self.number50_str).grid(row=5, column=1)
            tk.Label(master, text="mm").grid(row=5, column=2)
            # exemple de bouton ttk.Button(frm, text="►", command=root.destroy).grid(column=1, row=3)
            self.r9=ttk.Button(master, text="►", command=lambda:self.increase(2), width=10).grid(column=7, row=5)
            self.r10=ttk.Button(master, text="►►", command=self.mouvement, width=10).grid(column=8, row=5)
            self.r11=ttk.Button(master, text="◄", command=self.decrease, width=10).grid(column=5, row=5)
            self.r12=ttk.Button(master, text="◄◄", width=10).grid(column=4, row=5)       
            self.r13=ttk.Button(master, text="Home", width=10).grid(column=9, row=5)  
            self.r14=ttk.Button(master, text="█", width=10).grid(column=6, row=5) 
            
    
    
            # Sixth part the modification of the two engines
            
            tk.Label(master, text="").grid(column=10)
            tk.Label(master, text="").grid(row=6)
            frame = tk.Frame(self.master, width=50, height=50, highlightbackground="black", highlightthickness=2)
            frame.grid(row=0, column=11, rowspan=7)
            self.r15 = ttk.Button(frame, text="HOME", command=self.home, width=10).grid(column=0, row=0)
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
            
            tk.Label(master, text="").grid(row=10)
            
            
    
            #self.r20=ttk.Button(frame, text="Hexagon", width=10).grid(column=0, row=9)
            #self.r21=ttk.Button(frame, text="Circle", width=10).grid(column=0, row=10)   
            #self.r22=ttk.Button(frame, text="Line", width=10).grid(column=0, row=11)
            
            tk.Label(master, text="How many loop : ").grid(row=9, column=0)
            self.number_loop = ttk.Entry(frame, width=30)
            self.number_loop.grid(row=9, column=1, sticky="W", padx=5)
            self.r20 = ttk.Button(frame, text="ACCEPT", width=10, command=self.create_labels_and_entries)
            self.r20.grid(column=2, row=9)
            
            
            
            
            
        def create_labels_and_entries(self):
            # Récupérer le nombre de labels et d'entrys à créer
            num_entries = int(self.number_loop.get())
            i=0
            # Créer une nouvelle fenêtre
            window = tk.Toplevel()
            j=0
            k=0
            l=0
            self.Sleeptime = {}
            self.positionX = {}
            self.positionY = {}
            self.MovementTime = {}
            # Créer les labels et les entrys
            for i in range(num_entries):
                if l>=3:
                    l=0
                    j=0
                    label = ttk.Label(window, text="           ").grid(column=k+2)
                    label = ttk.Label(window, text="           ").grid(column=k+3)
                    k=k+4
                l=l+1   
        
                label = ttk.Label(window, text=f"Loop {i+1}").grid(row=j, column=k)
                label = ttk.Label(window, text=f"Sleep time (in s) :").grid(row=j+1, column=k)
                self.Sleeptime[i+1] = ttk.Entry(window)
                self.Sleeptime[i+1].grid(row=j+1, column=k+1)
                label = ttk.Label(window, text=f"Position x {i+1} (in mm) :").grid(row=j+2, column=k)
                self.positionAxis1 = ttk.Entry(window)
                self.positionAxis1.grid(row=j+2, column=k+1)
                label = ttk.Label(window, text=f"Position y {i+1} (in mm) :").grid(row=j+3, column=k)
                self.positionAxis2 = ttk.Entry(window)
                self.positionAxis2.grid(row=j+3, column=k+1)
                label = ttk.Label(window, text=f"Movement time (in s) :").grid(row=j+4, column=k)
                self.MovementTime[i+1] = ttk.Entry(window)
                self.MovementTime[i+1].grid(row=j+4, column=k+1)
                label = ttk.Label(window, text=" ").grid(row=j+5)
                j=j+6
            self.MovomentNow = ttk.Button(window, text="ACCEPT ALL", width=10, command=self.MovePlate).grid(row=16)
        
        def MovePlate(self):
            Movement=int(self.number_loop.get())
            
            for i in range(Movement):
                self.number150_str.set(str(axis1.get_position(Units.LENGTH_MILLIMETRES)))
                self.number50_str.set(str(axis2.get_position(Units.LENGTH_MILLIMETRES)))
                if self.Sleeptime[i+1].get()=="":
                    SleepTimeNow = 1
                    time.sleep(SleepTimeNow)
                elif self.Sleeptime[i+1].get()!="":
                    SleepTimeNow = float(self.Sleeptime[i+1].get())
                    time.sleep(SleepTimeNow)
                
                if self.positionAxis1.get() !="":
                    PositionNowAxis1 = float(self.positionAxis1.get())
                elif self.positionAxis1.get() =="":
                    PositionNowAxis1= axis1.get_position(Units.LENGTH_MILLIMETRES)
                    
                if self.positionAxis2.get() != "":
                    PositionNowAxis2 = float(self.positionAxis2.get())
                elif self.positionY[i+1].get() =="":
                    PositionNowAxis2= axis2.get_position(Units.LENGTH_MILLIMETRES)
                    
                if self.MovementTime[i+1].get() == "":
                    MovementTime = 10/2
                elif self.MovementTime[i+1].get() != "":
                    MovementTime = float(self.MovementTime[i+1].get())/2
                

                print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'")
                print(f"\nPosition axe 2 vérif :: '{axis2.get_position(Units.LENGTH_MILLIMETRES)}'")
                
                velocity1=abs(abs(PositionNowAxis1)-abs(axis1.get_position(Units.LENGTH_MILLIMETRES)))/MovementTime
                velocity2=abs(abs(PositionNowAxis2)-abs(axis2.get_position(Units.LENGTH_MILLIMETRES)))/MovementTime 
                
                random_number_step = random.uniform(0.0001, 0.000999)
                OldPositionX = axis1.get_position(Units.LENGTH_MILLIMETRES) 
                OldPositionY = axis2.get_position(Units.LENGTH_MILLIMETRES) 
                
                if PositionNowAxis1 > OldPositionX  and PositionNowAxis2 > OldPositionY:
                    if PositionNowAxis1 > OldPositionX:
                        axis1.move_absolute(PositionNowAxis1, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity1, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    
                    MovementTime = 10/2
                    
                    
                elif self.MovementTime[i+1].get() != "":
                    MovementTime = 10/2
                elif self.MovementTime[i+1].get() == "":
                    MovementTime = 10/2
                elif self.MovementTime[i+1].get() != "":
                    MovementTime = 10/2
                    
                    
 
                
                
                
                
                
                axis1.move_absolute(PositionNowAxis1, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity1, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)


                
                axis2.move_absolute(PositionNowAxis2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity2, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)



                number50 = axis2.get_position(Units.LENGTH_MILLIMETRES)
                number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                self.number50_str.set(str(number50))
                self.number150_str.set(str(number150))
                #test(axis1, axis2, self.number50_str, self.number150_str)
                print(f"\nPosition axe 1 :: '{number150}'")
                print(f"\nPosition axe 2 :: '{number50}'")
                
                self.r20.update()
                
                
        def home(self):
            
            axis1.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
            axis2.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
           
            self.number150_str.set(str(axis1.get_position(Units.LENGTH_MILLIMETRES)))
            self.number50_str.set(str(axis2.get_position(Units.LENGTH_MILLIMETRES)))            
            
        def home1(self):
            
            axis1.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
      
            self.number50_str.set(str(axis1.get_position(Units.LENGTH_MILLIMETRES)))
            self.number150_str.set(str(axis2.get_position(Units.LENGTH_MILLIMETRES)))    
            
        
        def increase(self, button_num):
            number50 = axis2.get_position(Units.LENGTH_MILLIMETRES)
            number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
            self.number50_str.set(str(number50))
            self.number150_str.set(str(number150))  
            print(f"\nPosition axe 1 :: '{number150}'")
            print(f"\nPosition axe 2 :: '{number50}'")
            
            if button_num == 1:
                    random_number_step = random.uniform(0.001, 0.00999)
                    for i in range(10):
                        number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                        axis1.move_absolute(number150+random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                        #axis1.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                        time.sleep(0.5)
                        number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                        number50 = axis2.get_position(Units.LENGTH_MILLIMETRES)    
                        print(f"\nPosition axe 1 :: '{number150}'")
                        self.update_labels(number150, number50)
            elif button_num == 2:
                
                axis2.move_max(wait_until_idle = True, velocity = 0, velocity_unit = Units.NATIVE, acceleration = 0, acceleration_unit = Units.NATIVE)
                #axis2.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
            number50 = axis1.get_position(Units.LENGTH_MILLIMETRES)
            number150 = axis2.get_position(Units.LENGTH_MILLIMETRES)    
            print(f"\nPosition axe 1 :: '{number50}'")
            print(f"\nPosition axe 2 :: '{number150}'")
            
            
        def decrease (self):
            #axis1.move_absolute(3, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
            i=0
            j=0
            for i in range(10):
                
                self.number50_str.set(i)
                print(f"\nNombre i :: '{i}'")
                if i >=2:
                    j=j+1
                    time.sleep(i-j)
            
        
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
                device.all_axes.stop()
                self.LSQ1.stop()
                self.LSQ2.stop()
            except AttributeError:
                # Axe non initialisé
                pass
    
        def distance_axe(self):
                position = axis.settings.get("encoder.pos")
                
        
        def update_labels(self, new_number150, new_number50):
                self.number150_str.set(str(new_number150))
                self.number50_str.set(str(new_number50))
    
    
    # Démarrage de la boucle principale
    root = tk.Tk()
    interface = Interface(root)
    
    root.mainloop()
