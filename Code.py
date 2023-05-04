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
            
            self.Check=tk.StringVar(value="")
            self.Check=1
            print(f"\nCheck : '{self.Check}'")
            
            self.number150_str.set(str(axis1.get_position(Units.LENGTH_MILLIMETRES)))
            self.number50_str.set(str(axis2.get_position(Units.LENGTH_MILLIMETRES)))
            
            self.Limit_MaxAxis1=60
            self.Limit_MaxAxis2=40
            
            axis1.settings.set("limit.max", 60, Units.LENGTH_MILLIMETRES)
            #axis1.settings.set("limit.max", 140, Units.LENGTH_MILLIMETRES)
            axis2.settings.set("limit.max", 40, Units.LENGTH_MILLIMETRES)
    
            print(f"\nPosition axe 1 : {self.number150_str.get()}")
            print(f"\nPosition axe 2 : {self.number50_str.get()}")
    
    
            # First part the number com and the connection button
            tk.Label(master, text="COM NUMBER :").grid(row=0, column=0)
            #self.connect_button = ttk.Button(master, text="Connection")
            #self.connect_button.grid(column=5, row=0)
            self.path_text = tk.Label(master, text="COM8", width=5)
            self.path_text.grid(row=0, column=1, sticky="W", padx=5, columnspan=4)
            self.disconnect_button = ttk.Button(master, text="Play", command=self.Check1to2)
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
           
            self.r3=ttk.Button(master, text="►", command=lambda:self.increase(1), width=10).grid(column=8, row=4)
            self.r4=ttk.Button(master, text="►►", width=10).grid(column=9, row=4)
            self.r10=ttk.Button(master, text="►|", command=self.increase(3), width=10).grid(column=10, row=4)
            self.r5=ttk.Button(master, text="◄", command=lambda:self.decrease(1), width=10).grid(column=6, row=4)
            self.r6=ttk.Button(master, text="◄◄", width=10).grid(column=5, row=4)     
            self.r10=ttk.Button(master, text="|◄", command=self.mouvement, width=10).grid(column=4, row=4)
            self.r7=ttk.Button(master, text="Home", command=lambda:self.home1(1), width=10).grid(column=11, row=4)  
            self.r8=ttk.Button(master, text="█", command=self.stop_all_axis, width=10).grid(column=7, row=4)  
    
    
            # Fifth part the 50 mm engine
            
            tk.Label(master, text="Motorized linear stage 50mm, Axis 2").grid(row=5, column=0)
            tk.Label(master, textvariable=self.number50_str).grid(row=5, column=1)
            tk.Label(master, text="mm").grid(row=5, column=2)
            # exemple de bouton ttk.Button(frm, text="►", command=root.destroy).grid(column=1, row=3)
            self.r9=ttk.Button(master, text="►", command=lambda:self.increase(2), width=10).grid(column=8, row=5)
            self.r10=ttk.Button(master, text="►►", command=self.mouvement, width=10).grid(column=9, row=5)
            self.r10=ttk.Button(master, text="►|", command=self.mouvement, width=10).grid(column=10, row=5)
            self.r11=ttk.Button(master, text="◄", command=lambda:self.decrease(2), width=10).grid(column=6, row=5)
            self.r12=ttk.Button(master, text="◄◄", width=10).grid(column=5, row=5)     
            self.r10=ttk.Button(master, text="|◄", command=self.mouvement, width=10).grid(column=4, row=5)
            self.r13=ttk.Button(master, text="Home", command=lambda:self.home1(2), width=10).grid(column=11, row=5)  
            self.r14=ttk.Button(master, text="█", width=10).grid(column=7, row=5) 
            
    
    
            # Sixth part the modification of the two engines
        
            tk.Label(master, text="").grid(column=16)
            tk.Label(master, text="").grid(row=6)
            frame = tk.Frame(self.master, width=50, height=50, highlightbackground="black", highlightthickness=2)
            frame.grid(row=0, column=11, rowspan=7)
            self.r15 = ttk.Button(frame, text="HOME", command=self.home, width=10).grid(column=0, row=0)
            self.r16 = ttk.Button(frame, text="█", command=self.stop_all_axis, width=10).grid(column=0, row=1)
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
            self.positionAxis1_ = {}
            self.positionAxis2_ = {}
            self.MovementTime = {}
            # Créer les labels et les entrys
            Move=num_entries
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
                label = ttk.Label(window, text=f"Position Axis1 {i+1} (in mm) :").grid(row=j+2, column=k)
                self.positionAxis1_[i+1] = ttk.Entry(window)
                self.positionAxis1_[i+1].grid(row=j+2, column=k+1)
                label = ttk.Label(window, text=f"Position Axis2 {i+1} (in mm) :").grid(row=j+3, column=k)
                self.positionAxis2_[i+1] = ttk.Entry(window)
                self.positionAxis2_[i+1].grid(row=j+3, column=k+1)
                label = ttk.Label(window, text=f"Movement time (in s) :").grid(row=j+4, column=k)
                self.MovementTime[i+1] = ttk.Entry(window)
                self.MovementTime[i+1].grid(row=j+4, column=k+1)
                label = ttk.Label(window, text=" ").grid(row=j+5)
                j=j+6
            self.MovomentNow = ttk.Button(window, text="ACCEPT ALL", width=10, command=lambda: self.MovePlate(num_entries)).grid(row=20)
        
        def MovePlate(self, Movement):
            #Movement=num_entries
            print(f"\nnum_entries :: '{Movement}'")
            for i in range(Movement):
                random_number_step = round(random.uniform(0.01, 0.09999), 5)
                print(f"\nRandom_number_step :: '{random_number_step}'")
                self.number150_str.set(str(axis1.get_position(Units.LENGTH_MILLIMETRES)))
                self.number50_str.set(str(axis2.get_position(Units.LENGTH_MILLIMETRES)))
                if self.Sleeptime[i+1].get()=="":
                    SleepTimeNow = 1
                elif self.Sleeptime[i+1].get()!="":
                    SleepTimeNow = float(self.Sleeptime[i+1].get())
                
                if self.positionAxis2_[i+1].get() != "":
                    PositionNowAxis2 = float(self.positionAxis2_[i+1].get())
                    if PositionNowAxis2==0:
                        PositionNowAxis2=0.00001
                elif self.positionAxis2_[i+1].get() =="":
                    PositionNowAxis2= axis2.get_position(Units.LENGTH_MILLIMETRES)
                
                
                
                if self.positionAxis1_[i+1].get() !="":
                    PositionNowAxis1 = float(self.positionAxis1_[i+1].get())
                    if PositionNowAxis1==0:
                        PositionNowAxis1=0.00001
                    
                    
                    
                    
                    
                elif self.positionAxis1_[i+1].get() =="":
                    PositionNowAxis1= axis1.get_position(Units.LENGTH_MILLIMETRES)
                    
                    
            
            
            
                    
                if self.MovementTime[i+1].get() == "":
                    MovementTime = 20/2
                    if abs(PositionNowAxis1-axis1.get_position(Units.LENGTH_MILLIMETRES))<0.5 or abs(PositionNowAxis2-axis2.get_position(Units.LENGTH_MILLIMETRES))<0.5:
                        MovementTime = 6/2
                elif self.MovementTime[i+1].get() != "":
                    MovementTime = float(self.MovementTime[i+1].get())/2

                

                print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'")
                print(f"\nPosition axe 2 vérif :: '{axis2.get_position(Units.LENGTH_MILLIMETRES)}'")
               
                
                TimeByStep=(abs(random_number_step)*MovementTime)/(abs(axis1.get_position(Units.LENGTH_MILLIMETRES) - PositionNowAxis1)+1)         
                velocity0= random_number_step/TimeByStep
                OldPositionX = axis1.get_position(Units.LENGTH_MILLIMETRES) 
                OldPositionY = axis2.get_position(Units.LENGTH_MILLIMETRES) 
                quotient, remainder = divmod(abs(PositionNowAxis1-axis1.get_position(Units.LENGTH_MILLIMETRES)+1), random_number_step)
                integer_part = quotient-1
                decimal_part = remainder / random_number_step
                
                random_number_step2 = (abs(PositionNowAxis2-axis2.get_position(Units.LENGTH_MILLIMETRES)))/quotient   
                             
                quotient2, remainder = divmod(abs(PositionNowAxis2-axis2.get_position(Units.LENGTH_MILLIMETRES)+1), random_number_step2)
                integer_part2 = quotient2-1
                decimal_part2 = remainder / random_number_step2              
                
                
                
                
                time.sleep(SleepTimeNow)
                if abs(OldPositionX - PositionNowAxis1) > 0.01 or abs(OldPositionY - PositionNowAxis2) > 0.01:
                    

                    
                    print(f"\n integer_part :: '{integer_part}'")
                    i=0
                    
                    if abs(OldPositionX - PositionNowAxis1) >= 0.01 and abs(OldPositionY - PositionNowAxis2) >= 0.01:
                        if OldPositionX < PositionNowAxis1 and OldPositionY < PositionNowAxis2 :
                            #à envoyer : MovementTime, integer_part,decimal_part, random_number_step, la velocité nommé velocity0, ConfigureNumber (dans quel "if" on est), 
                            self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, 1)
                          
                        elif OldPositionX > PositionNowAxis1 and OldPositionY < PositionNowAxis2 :
                            self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, 2)
                        elif OldPositionX < PositionNowAxis1 and OldPositionY > PositionNowAxis2 :
                            self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, 3)
                        elif OldPositionX > PositionNowAxis1 and OldPositionY > PositionNowAxis2 :    
                            self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, 4)
                            
                          
                        
                    elif abs(OldPositionX - PositionNowAxis1) >= 0.01 and abs(OldPositionY - PositionNowAxis2) <= 0.01:
                        if OldPositionX < PositionNowAxis1 :
                            self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, 5)
                          
                        elif OldPositionX > PositionNowAxis1 :
                            self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, 6)
                        
                        
                        
                    elif abs(OldPositionX - PositionNowAxis1) <= 0.01 and abs(OldPositionY - PositionNowAxis2) >= 0.01:
                        if OldPositionY < PositionNowAxis2 :
                            self.mouvement_Move_Plate(MovementTime, integer_part2, decimal_part2, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, 7)
                          
                        elif OldPositionY > PositionNowAxis2 :
                            self.mouvement_Move_Plate(MovementTime, integer_part2, decimal_part2, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, 8)
                        
                        
                        
                number50 = axis2.get_position(Units.LENGTH_MILLIMETRES)
                number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                #print(f"\nPosition axe 1 :: '{number150}'")
                #print(f"\nPosition axe 2 :: '{number50}'")
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                
        
                
        def mouvement_Move_Plate (self, MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, ConfigureNumber):
                  
            if ConfigureNumber == 1:
                i=0
                while i<integer_part and self.Check == 1:
                    number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                    axis1.move_relative(random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(random_number_step2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                if self.Check==1:    
                    axis1.move_relative(random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(random_number_step2*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis 
                    
            elif ConfigureNumber == 2:
                i=0
                while i<integer_part and self.Check == 1:
                    number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                    axis1.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(random_number_step2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                if self.Check==1:    
                    axis1.move_relative(-random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis 
                    
            elif ConfigureNumber == 3:
                i=0
                while i<integer_part and self.Check == 1:
                    number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                    axis1.move_relative(random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(-random_number_step2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                if self.Check==1:    
                    axis1.move_relative(random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis 
                    
            elif ConfigureNumber == 4:
                i=0
                while i<integer_part and self.Check == 1:
                    number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                    axis1.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(-random_number_step2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                if self.Check==1:    
                    axis1.move_relative(-random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis 
                    
            elif ConfigureNumber == 5:
                i=0
                while i<integer_part and self.Check == 1:
                    axis1.move_relative(random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                if self.Check==1:    
                    axis1.move_relative(random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis 
                    
            elif ConfigureNumber == 6:
                i=0
                while i<integer_part and self.Check == 1:
                    axis1.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                if self.Check==1:    
                    axis1.move_relative(-random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis 
            
            elif ConfigureNumber == 7:
                i=0
                while i<integer_part and self.Check == 1:
                    print("\n Nous sommes dans le configure number7")
                    axis2.move_relative(random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)                    
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                if self.Check == 2:
                    self.stop_all_axis 
                    
            elif ConfigureNumber == 8:
                i=0
                while i<integer_part and self.Check == 1:
                    print("\n Nous sommes dans le configure number8")
                    axis2.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)                    
                    i=i+1
                    axis2.move_relative(-random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                if self.Check == 2:
                    self.stop_all_axis 
                    
                    
        
        def home(self):
            axis1.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
            axis2.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))          
            
        def home1(self, number):
            
            if number==1:    
                axis1.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                print(f"\nPosition axe 1 : {self.number150_str.get()}")
            elif number==2:
                axis2.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                print(f"\nPosition axe 2 : {self.number50_str.get()}")
                
            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
            
        
        def increase10(self, number):
            if number==1:    
                axis1.move_relative(10, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                print(f"\nPosition axe 1 : {self.number150_str.get()}")
            elif number==2:
                axis2.move_relative(10, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                print(f"\nPosition axe 2 : {self.number50_str.get()}")
  
        
        
        def increase(self, button_num):
            number50 = axis2.get_position(Units.LENGTH_MILLIMETRES)
            number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
            self.number50_str.set(str(number50))
            self.number150_str.set(str(number150))  
            print(f"\nPosition axe 1 :: '{number150}'")
            print(f"\nPosition axe 2 :: '{number50}'")
            i=0
            if button_num == 1:
                    
                    while i < 20 and self.Check == 1:
                            i=i+1
                            self.master.update()
                            print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                            axis1.move_relative(0.5, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                    if self.Check==2:
                            self.stop_all_axis
            elif button_num == 2:

                    while i < 20 and self.Check == 1:
                        i=i+1
                        self.master.update()
                        print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                        axis2.move_relative(0.5, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                        self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                        self.master.update()
                    
                    if self.Check==2:
                            self.stop_all_axis

            elif button_num == 3:
                    NumberStep=5
                    quotient, remainder = divmod(abs(self.Limit_MaxAxis1-axis1.get_position(Units.LENGTH_MILLIMETRES)+1), NumberStep)
                    integer_part = quotient-1
                    decimal_part = remainder / NumberStep
                    
                    while i < integer_part and self.Check == 1:
                            i=i+1
                            
                            self.master.update()
                            print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                            axis1.move_relative(NumberStep, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                            
                    if self.Check==1:    
                        axis1.move_relative(NumberStep*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                
                    if self.Check==2:
                            self.stop_all_axis        
                            
                            
                            
                            
            number50 = axis1.get_position(Units.LENGTH_MILLIMETRES)
            number150 = axis2.get_position(Units.LENGTH_MILLIMETRES)    
            print(f"\nPosition axe 1 :: '{number50}'")
            print(f"\nPosition axe 2 :: '{number150}'")
                        
                            
                            
                            
                            
                            
                            
            
        def decrease (self, button_num):
            number50 = axis2.get_position(Units.LENGTH_MILLIMETRES)
            number150 = axis1.get_position(Units.LENGTH_MILLIMETRES)
            self.number50_str.set(str(number50))
            self.number150_str.set(str(number150))  
            print(f"\nPosition axe 1 :: '{number150}'")
            print(f"\nPosition axe 2 :: '{number50}'")
            i=0
            if button_num == 1:
                    
                    while i < 20 and self.Check == 1:
                        i=i+1
                        self.master.update()
                        print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                        axis1.move_relative(-0.5, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                        self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                        self.master.update()
                    if self.Check==2:
                            self.stop_all_axis
            elif button_num == 2:

                    while i < 20 and self.Check == 1:
                        i=i+1
                        self.master.update()
                        print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                        axis2.move_relative(-0.5, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                        self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                        self.master.update()
                    if self.Check==2:
                            self.stop_all_axis
            number50 = axis1.get_position(Units.LENGTH_MILLIMETRES)
            number150 = axis2.get_position(Units.LENGTH_MILLIMETRES)    
            print(f"\nPosition axe 1 :: '{number50}'")
            print(f"\nPosition axe 2 :: '{number150}'")
            
        
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
    
        def stop_all_axis(self):
            try:
                if self.Check==1:
                    device.all_axes.stop()
                    self.master.update()
                    self.Check=2
                    self.master.update()
                    print(f"\nStop : '{self.Check}'")
                if self.Check==2:
                    device.all_axes.stop()
            except AttributeError:
                # Axe non initialisé
                pass              
        
        def update_labels(self, new_number150, new_number50):
            self.number150_str.set(str(new_number150))
            self.number50_str.set(str(new_number50))
            self.master.update()
    
        def Check1to2(self):
            self.Check = 1
            print(f"\n Check : '{self.Check}'")
            
            
            
            
    # Démarrage de la boucle principale
    root = tk.Tk()
    interface = Interface(root)
    
    root.mainloop()
