# You have to download since the "Python\Python311\Lib\site-packages" many
# different libraries named : zaber, zaber.serial-0.9.1.dist-info, zaber_motion,
# zaber_motion_bindings_windows, zaber_motion_bindings_windows-3.1.1.dist-info,
# zaber_motion-3.1.1.dist-info, tkinter, time, serial.tools.list_ports, serial.
# You can also take this library since another computer and paste it in the
# "site-packages" file.

'''
import tkinter as tk

def check():
    if var.get() == 1:
        label.config(text="La case est cochée.")
    else:
        label.config(text="La case n'est pas cochée.")

root = tk.Tk()

var = tk.IntVar()
checkbox = tk.Checkbutton(root, text="Case à cocher", variable=var, command=check)
checkbox.pack()

label = tk.Label(root, text="")
label.pack()

root.mainloop()
'''



import decimal
import math
import tkinter.filedialog as filedialog
import tkinter as tk
import subprocess
import zaber_motion
import serial.tools.list_ports as list_ports
import time
import random


from decimal import Decimal
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
            
            self.Limit_MaxAxis1=Decimal(148.5000000000)
            self.Limit_MaxAxis2=Decimal(48.500000000)
            
            self.Limit_MinAxis1=Decimal(1.0000000000)
            self.Limit_MinAxis2=Decimal(1.0000000000)
            
            axis1.settings.set("limit.max", self.Limit_MaxAxis1, Units.LENGTH_MILLIMETRES)
            axis2.settings.set("limit.max", self.Limit_MaxAxis2, Units.LENGTH_MILLIMETRES)
    
            print(f"\nPosition axe 1 : {self.number150_str.get()}")
            print(f"\nPosition axe 2 : {self.number50_str.get()}")
    
    
            # First part the number com and the connection button
            tk.Label(master, text="COM NUMBER :").grid(row=0, column=0)
            #self.connect_button = ttk.Button(master, text="Connection")
            #self.connect_button.grid(column=5, row=0)
            self.path_text = tk.Label(master, text="COM8", width=5)
            self.path_text.grid(row=0, column=1, sticky="W", padx=5, columnspan=4)
            self.disconnect_button = ttk.Button(master, text="Unlock", command=self.Check1to2)
            self.disconnect_button.grid(column=6, row=0)
            
            self.case = tk.Frame(self.master, width=50, height=50, bg="green")
            self.case.grid(row=0, column=8)
            
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
            self.r4=ttk.Button(master, text="►►", command=lambda:self.mouvement_Move_Plate (0, 0, 0, 0, 0, 0, 0, 0, 9), width=10).grid(column=9, row=4)
            self.r10=ttk.Button(master, text="►|", command=lambda:self.increase(3), width=10).grid(column=10, row=4)
            self.r5=ttk.Button(master, text="◄", command=lambda:self.decrease(1), width=10).grid(column=6, row=4)
            self.r6=ttk.Button(master, text="◄◄",command=lambda:self.mouvement_Move_Plate (0, 0, 0, 0, 0, 0, 0, 0, 10), width=10).grid(column=5, row=4)     
            self.r10=ttk.Button(master, text="|◄", command=lambda:self.mouvement, width=10).grid(column=4, row=4)
            self.r7=ttk.Button(master, text="Home", command=lambda:self.home1(1), width=10).grid(column=11, row=4)  
            self.r8=ttk.Button(master, text="█", command=lambda:self.StopAxis(1), width=10).grid(column=7, row=4)  
    
    
            # Fifth part the 50 mm engine
            
            tk.Label(master, text="Motorized linear stage 50mm, Axis 2").grid(row=5, column=0)
            tk.Label(master, textvariable=self.number50_str).grid(row=5, column=1)
            tk.Label(master, text="mm").grid(row=5, column=2)
            # exemple de bouton ttk.Button(frm, text="►", command=root.destroy).grid(column=1, row=3)
            self.r9=ttk.Button(master, text="►", command=lambda:self.increase(2), width=10).grid(column=8, row=5)
            self.r10=ttk.Button(master, text="►►", command=lambda:self.mouvement_Move_Plate (0, 0, 0, 0, 0, 0, 0, 0, 11),  width=10).grid(column=9, row=5)
            self.r10=ttk.Button(master, text="►|", command=lambda:self.increase(4), width=10).grid(column=10, row=5)
            self.r11=ttk.Button(master, text="◄", command=lambda:self.decrease(2), width=10).grid(column=6, row=5)
            self.r12=ttk.Button(master, text="◄◄", command=lambda:self.mouvement_Move_Plate (0, 0, 0, 0, 0, 0, 0, 0, 12), width=10).grid(column=5, row=5)     
            self.r10=ttk.Button(master, text="|◄", command=lambda:self.mouvement, width=10).grid(column=4, row=5)
            self.r13=ttk.Button(master, text="Home", command=lambda:self.home1(2), width=10).grid(column=11, row=5)  
            self.r14=ttk.Button(master, text="█", command=lambda:self.StopAxis(2), width=10).grid(column=7, row=5) 
            
    
    
            # Sixth part the modification of the two engines
        
            tk.Label(master, text="").grid(column=12)
            tk.Label(master, text="").grid(row=6)
            frame = tk.Frame(self.master, width=50, height=50, highlightbackground="black", highlightthickness=2)
            frame.grid(row=0, column=13, rowspan=7)
            self.r15 = ttk.Button(frame, text="HOME", command=lambda:self.home(), width=10).grid(column=0, row=0)
            self.r16 = ttk.Button(frame, text="█", command=lambda:self.stop_all_axis(), width=10).grid(column=0, row=1)
            tk.Label(frame, text="").grid(column=1, row= 0)
            
            
            tk.Label(frame, text="Move to absolute position").grid(row=0, column=3)
            self.number_text_AbsolutePosition = ttk.Entry(frame, width=30)
            self.number_text_AbsolutePosition.grid(row=1, column=3, sticky="W", padx=5)
            self.r17=ttk.Button(frame, text="►", command=lambda:self.TwoDevice(1), width=10).grid(column=5, row=1)
            tk.Label(frame, text="mm").grid(row=1, column=4)
    
    
            tk.Label(frame, text="").grid(row=2)
            tk.Label(frame, text="Move by relative position").grid(row=4, column=3)
            self.number_text_RelativePosition = ttk.Entry(frame, width=30)
            self.number_text_RelativePosition.grid(row=5, column=3, sticky="W", padx=5)
            self.r18=ttk.Button(frame, text="►", command=lambda:self.TwoDevice(2), width=10).grid(column=5, row=5)
            self.r19=ttk.Button(frame, text="◄", command=lambda:self.TwoDevice(3), width=10).grid(column=2, row=5)
            tk.Label(frame, text="mm").grid(row=5, column=4)
    
            tk.Label(frame, text="").grid(row=6)
            tk.Label(frame, text="Move at velocity").grid(row=7, column=3)
            self.number_text_RelativeVelocity = ttk.Entry(frame, width=30)
            self.number_text_RelativeVelocity.grid(row=8, column=3, sticky="W", padx=5)
            self.r18=ttk.Button(frame, text="►", command=lambda:self.TwoDevice(4), width=10).grid(column=5, row=8)
            self.r19=ttk.Button(frame, text="◄", command=lambda:self.TwoDevice(5), width=10).grid(column=2, row=8)
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
            
            

            self.r21 = ttk.Button(frame, text="CIRCLE", width=10, command=self.circle)
            self.r21.grid(column=7, row=9)
            
            
            
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
            for i in range(num_entries):
                if l>=3:
                    l=0
                    j=0
                    label = ttk.Label(window, text="           ").grid(column=k+2)
                    label = ttk.Label(window, text="           ").grid(column=k+3)
                    k=k+4
                l=l+1   
        
                label = ttk.Label(window, text=f"Loop {i+1}").grid(row=j, column=k)
                label = ttk.Label(window, text="Sleep time (in s) :").grid(row=j+1, column=k)
                self.Sleeptime[i+1] = ttk.Entry(window)
                self.Sleeptime[i+1].grid(row=j+1, column=k+1)
                label = ttk.Label(window, text=f"Position Axis1 {i+1} (in mm) :").grid(row=j+2, column=k)
                self.positionAxis1_[i+1] = ttk.Entry(window)
                self.positionAxis1_[i+1].grid(row=j+2, column=k+1)
                label = ttk.Label(window, text=f"Position Axis2 {i+1} (in mm) :").grid(row=j+3, column=k)
                self.positionAxis2_[i+1] = ttk.Entry(window)
                self.positionAxis2_[i+1].grid(row=j+3, column=k+1)
                label = ttk.Label(window, text="Movement time (in s) :").grid(row=j+4, column=k)
                self.MovementTime[i+1] = ttk.Entry(window)
                self.MovementTime[i+1].grid(row=j+4, column=k+1)
                label = ttk.Label(window, text=" ").grid(row=j+5)
                j=j+6
            self.MovomentNow = ttk.Button(window, text="ACCEPT ALL", width=15, command=lambda: self.MovePlate(num_entries)).grid(row=20)
        
        def MovePlate(self, Movement):
            #Movement=num_entries
            print(f"\n num_entries :: '{Movement}'")
            for i in range(Movement):
                random_number_step = Decimal(round(random.uniform(0.0001000, 0.0009999), 7))
                print(f"\nRandom_number_step :: '{random_number_step}'")
                self.number150_str.set(str(axis1.get_position(Units.LENGTH_MILLIMETRES)))
                self.number50_str.set(str(axis2.get_position(Units.LENGTH_MILLIMETRES)))
                if self.Sleeptime[i+1].get()=="":
                    SleepTimeNow = 1
                elif self.Sleeptime[i+1].get()!="":
                    SleepTimeNow = Decimal(self.Sleeptime[i+1].get())
                
                if self.positionAxis2_[i+1].get() != "":
                    PositionNowAxis2 = Decimal(self.positionAxis2_[i+1].get())
                    if PositionNowAxis2==0:
                        PositionNowAxis2=Decimal(0.00001)
                elif self.positionAxis2_[i+1].get() =="":
                    PositionNowAxis2= axis2.get_position(Units.LENGTH_MILLIMETRES)
                
                
                
                if self.positionAxis1_[i+1].get() !="":
                    PositionNowAxis1 = float(self.positionAxis1_[i+1].get())
                    if PositionNowAxis1==0:
                        PositionNowAxis1=Decimal(0.00001)
                    
                    
                    
                    
                    
                elif self.positionAxis1_[i+1].get() =="":
                    PositionNowAxis1= axis1.get_position(Units.LENGTH_MILLIMETRES)
                    
                    
                if self.MovementTime[i+1].get() == "":
                    MovementTime = 20/2
                    if abs(PositionNowAxis1-axis1.get_position(Units.LENGTH_MILLIMETRES))<0.5 or abs(PositionNowAxis2-axis2.get_position(Units.LENGTH_MILLIMETRES))<0.5:
                        MovementTime = 6/2
                elif self.MovementTime[i+1].get() != "":
                    MovementTime = Decimal(self.MovementTime[i+1].get())/2

                

                print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'")
                print(f"\nPosition axe 2 vérif :: '{axis2.get_position(Units.LENGTH_MILLIMETRES)}'")
               
                
                TimeByStep=Decimal(abs(random_number_step)*MovementTime)/(abs(axis1.get_position(Units.LENGTH_MILLIMETRES) - PositionNowAxis1)+1)         
                velocity0= Decimal(random_number_step/TimeByStep)
                OldPositionX = axis1.get_position(Units.LENGTH_MILLIMETRES) 
                OldPositionY = axis2.get_position(Units.LENGTH_MILLIMETRES) 
                quotient, remainder = Decimal(divmod(abs(PositionNowAxis1-axis1.get_position(Units.LENGTH_MILLIMETRES)+0.01), random_number_step))
                integer_part = quotient-1
                decimal_part = Decimal(remainder / random_number_step)
                
                random_number_step2 = Decimal((abs(PositionNowAxis2-axis2.get_position(Units.LENGTH_MILLIMETRES)))/quotient   )
                             
                quotient2, remainder = divmod(abs(PositionNowAxis2-axis2.get_position(Units.LENGTH_MILLIMETRES)+0.01), random_number_step2)
                integer_part2 = quotient2-1
                decimal_part2 = remainder / random_number_step2              
                
                print(f"\n decimal_part :: '{decimal_part}'") 
                
                
                time.sleep(SleepTimeNow)
                if abs(OldPositionX - PositionNowAxis1) > 0.01 or abs(OldPositionY - PositionNowAxis2) > 0.01:
                    

                    
                    print(f"\n integer_part :: '{integer_part}'")
                    i=0
                    
                    if abs(OldPositionX - PositionNowAxis1) >= 0.01 and abs(OldPositionY - PositionNowAxis2) >= 0.01:
                        
                        if OldPositionX < PositionNowAxis1 and OldPositionY < PositionNowAxis2 :
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
                        
                        
                        
                #print(f"\nPosition axe 1 :: '{number150}'")
                #print(f"\nPosition axe 2 :: '{number50}'")
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                
        
                
        def mouvement_Move_Plate (self, MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, PositionNowAxis1, PositionNowAxis2, velocity0, ConfigureNumber):
                  
            if ConfigureNumber == 1:
                i=0
                while i<integer_part and self.Check == 1:
              
                    axis1.move_relative(random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(random_number_step2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                if self.Check==1:    
                    axis1.move_relative(random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(random_number_step2*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis ()
                    
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))    
            elif ConfigureNumber == 2:
                i=0
                while i<integer_part and self.Check == 1:
                 
                    axis1.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(random_number_step2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                 
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                if self.Check==1:    
                    axis1.move_relative(-random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis ()
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))    
            elif ConfigureNumber == 3:
                i=0
                while i<integer_part and self.Check == 1:
  
                    axis1.move_relative(random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(-random_number_step2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)

                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                if self.Check==1:    
                    axis1.move_relative(random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis ()
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))    
            elif ConfigureNumber == 4:
                i=0
                while i<integer_part and self.Check == 1:

                    axis1.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    axis2.move_relative(-random_number_step2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)

                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                if self.Check==1:    
                    axis1.move_relative(-random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis() 
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))    
            elif ConfigureNumber == 5:
                i=0
                while i<integer_part and self.Check == 1:
                    axis1.move_relative(random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                if self.Check==1:    
                    axis1.move_relative(random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis ()
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))    
            elif ConfigureNumber == 6:
                i=0
                while i<integer_part and self.Check == 1:
                    axis1.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                        
                if self.Check==1:    
                    axis1.move_relative(-random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis() 
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
            elif ConfigureNumber == 7:
                i=0
                while i<integer_part and self.Check == 1:
                    axis2.move_relative(random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)                    
                    i=i+1
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                if self.Check == 2:
                    self.stop_all_axis()
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))    
            elif ConfigureNumber == 8:
                i=0
                while i<integer_part and self.Check == 1:
                    axis2.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)                    
                    i=i+1
                    axis2.move_relative(-random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                if self.Check == 2:
                    self.stop_all_axis()
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
            
            
            elif ConfigureNumber == 9:
                MovementTime=5
                random_number_step=0.6
                TimeByStep=(abs(random_number_step)*MovementTime)/(abs(axis1.get_position(Units.LENGTH_MILLIMETRES) - self.Limit_MaxAxis1)+1)         
                velocity0= random_number_step/TimeByStep
                quotient, remainder = divmod(abs(self.Limit_MaxAxis1-axis1.get_position(Units.LENGTH_MILLIMETRES)+0.01), random_number_step)
                integer_part = quotient-1
                decimal_part = remainder / random_number_step
                
                while axis1.get_position(Units.LENGTH_MILLIMETRES)+1<self.Limit_MaxAxis1 and self.Check == 1:
                    axis1.move_relative(random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)

                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                    
                if axis1.get_position(Units.LENGTH_MILLIMETRES)+(random_number_step*(decimal_part+1))<self.Limit_MaxAxis1 and self.Check==1:    
                    axis1.move_relative(random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                if self.Check == 2:
                    self.stop_all_axis()
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                
                
            elif ConfigureNumber == 10:
                MovementTime=5
                random_number_step=0.525
                TimeByStep=(abs(random_number_step)*MovementTime)/(abs(axis1.get_position(Units.LENGTH_MILLIMETRES) - self.Limit_MaxAxis1)+1)         
                velocity0= random_number_step/TimeByStep
                quotient, remainder = divmod(abs(self.Limit_MaxAxis1-axis1.get_position(Units.LENGTH_MILLIMETRES)+0.01), random_number_step)
                integer_part = quotient-1
                decimal_part = remainder / random_number_step
                
                while axis1.get_position(Units.LENGTH_MILLIMETRES)>self.Limit_MinAxis1+1 and self.Check == 1:
                    axis1.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                    
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                if self.Check==1:    
                    axis1.move_absolu(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                
                
                if self.Check == 2:
                    self.stop_all_axis()
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                
                
                
            elif ConfigureNumber == 11:
                MovementTime=5
                random_number_step=0.525
                TimeByStep=(abs(random_number_step)*MovementTime)/(abs(axis2.get_position(Units.LENGTH_MILLIMETRES) - self.Limit_MaxAxis2)+1)         
                velocity0= random_number_step/TimeByStep
                quotient, remainder = divmod(abs(self.Limit_MaxAxis2-axis2.get_position(Units.LENGTH_MILLIMETRES)+0.01), random_number_step)
                integer_part = quotient-1
                decimal_part = remainder / random_number_step
                
                while axis2.get_position(Units.LENGTH_MILLIMETRES)<self.Limit_MaxAxis2 and self.Check == 1:
                    axis2.move_relative(random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                    
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    
                if self.Check==1 and axis2.get_position(Units.LENGTH_MILLIMETRES)+(random_number_step*(decimal_part+1))<self.Limit_MaxAxis2:    
                     axis2.move_relative(random_number_step*(decimal_part+1), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                
                
                if self.Check == 2:
                    self.stop_all_axis()
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                
            elif ConfigureNumber == 12:
                MovementTime=5
                random_number_step=0.525
                TimeByStep=(abs(random_number_step)*MovementTime)/(abs(axis2.get_position(Units.LENGTH_MILLIMETRES) - self.Limit_MaxAxis2)+1)         
                velocity0= random_number_step/TimeByStep
                quotient, remainder = divmod(abs(self.Limit_MaxAxis2-axis2.get_position(Units.LENGTH_MILLIMETRES)+0.01), random_number_step)
                integer_part = quotient-1
                decimal_part = remainder / random_number_step
                
                while axis2.get_position(Units.LENGTH_MILLIMETRES)>self.Limit_MinAxis2+1 and self.Check == 1:
                    axis2.move_relative(-random_number_step, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=velocity0/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                    if self.Check == 2:
                        self.stop_all_axis()
                        break
                if self.Check==1:    
                    axis2.move_absolu(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = velocity0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                
                
                if self.Check == 2:
                    self.stop_all_axis()
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                

        
        def home(self):
            print("test")
            increment_value = Decimal("0.00000001")
            i=0
            random_number_step1=Decimal(0.300000)
            quotient, remainder = (divmod(abs(Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES))+ increment_value), random_number_step1))
            integer_part = quotient-1
            decimal_part = Decimal(remainder / random_number_step1)   
            
            if axis1.get_position(Units.LENGTH_MILLIMETRES)>self.Limit_MinAxis1+1 and self.Check == 1:
                random_number_step2 = ((abs(Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES)))+ increment_value)/quotient)
            
                while i < integer_part-1 and self.Check == 1:
                    i=i+1
                    axis1.move_relative(-random_number_step1, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    if axis2.get_position(Units.LENGTH_MILLIMETRES)>self.Limit_MinAxis2+1:
                        axis2.move_relative(-random_number_step2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))   
                    if self.Check == 2:
                            self.stop_all_axis()
                            break
                    
            elif axis1.get_position(Units.LENGTH_MILLIMETRES) < self.Limit_MinAxis1+1 and axis2.get_position(Units.LENGTH_MILLIMETRES) > self.Limit_MinAxis2+1 and self.Check == 1:
                quotient, remainder =(divmod(abs(Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES)))+ increment_value, random_number_step1))
                integer_part = quotient-1
                decimal_part = Decimal(remainder / random_number_step1)              
                
                while i < integer_part-1 and self.Check == 1:
                    i=i+1
                    axis2.move_relative(-random_number_step1, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))                 
                    if self.Check == 2:
                            self.stop_all_axis()
                            break
                
            
            if self.Check == 2:
                self.stop_all_axis()
                
                    
            if self.Check == 1:
                axis1.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                axis2.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))          
            
        def home1(self, number):
            increment_value = Decimal("0.00000001")
            i=0
            
            if number==1 :
                random_number_step1=Decimal(0.300000)
                quotient, remainder = (divmod(abs(Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES))+ increment_value), random_number_step1))
                integer_part = quotient-1
                #print(f"\n integer_part {integer_part}")
                while i < integer_part-1 and self.Check == 1 and axis1.get_position(Units.LENGTH_MILLIMETRES)>self.Limit_MinAxis1+1 :
                    i=i+1
                    axis1.move_relative(-random_number_step1, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))  
                    
                        
                if self.Check == 1 and (abs(axis1.get_position(Units.LENGTH_MILLIMETRES)))>0.3 :
                    axis1.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)     
                   
                    
                   
            elif number==2 :
                random_number_step1=Decimal(0.300000)
                quotient, remainder = divmod(abs(Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))+increment_value), random_number_step1)
                integer_part = quotient-1                
                
                while i < integer_part-1 and self.Check == 1 and axis2.get_position(Units.LENGTH_MILLIMETRES)>self.Limit_MinAxis2+1 :
                    i=i+1
                    axis2.move_relative(-random_number_step1, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity=0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                    self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))                 
                
                if self.Check == 1 and (abs(axis2.get_position(Units.LENGTH_MILLIMETRES)))>0.3 :
                    axis2.move_absolute(0, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
     
            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
            
        
        
        def increase(self, button_num):
            increment_value = Decimal("0.00000001")
            number50 = Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))
            number150 = Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES))
            self.number50_str.set(str(number50))
            self.number150_str.set(str(number150))  
            #print(f"\nPosition axe 1 :: '{number150}'")
            #print(f"\nPosition axe 2 :: '{number50}'")
            i=0
            if button_num == 1:
                    
                    while i < 20 and self.Check == 1:
                            increase = Decimal(0.5000000)
                            i=i+1
                            self.master.update()
                            print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                            axis1.move_relative(increase, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                            if self.Check==2:
                                    self.stop_all_axis()
                                    break
            elif button_num == 2:

                    while i < 20 and self.Check == 1:
                            increase = Decimal(0.5000000)
                            i=i+1
                            self.master.update()
                            print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                            axis2.move_relative(increase, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0.9, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                    
                            if self.Check==2:
                                    self.stop_all_axis()
                                    break

            elif button_num == 3:
                    NumberStep=Decimal(1.00000)
                    Security=Decimal(0.90000)
                    quotient, remainder = divmod(abs((self.Limit_MaxAxis1- Security)-Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES))+increment_value), NumberStep)

                    integer_part = quotient-1
                    decimal_part = Decimal(remainder / NumberStep)
                    while i < integer_part and self.Check == 1:
                            i=i+1
                            
                            self.master.update()
                            print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                            axis1.move_relative(NumberStep, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 1, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                            
                            if self.Check==1 and abs((self.Limit_MaxAxis1+Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES))))>0.3 :    
                                axis1.move_absolute(self.Limit_MaxAxis1, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                      
                            if self.Check==2:
                                    self.stop_all_axis()
                                    break
                            

            elif button_num == 4:
                    NumberStep=Decimal(1.00000)
                    Security=Decimal(0.90000)
                    quotient, remainder = divmod(abs((self.Limit_MaxAxis2- Security)-axis2.get_position(Units.LENGTH_MILLIMETRES)+0.01), NumberStep)
                    integer_part = quotient-1
                    decimal_part = Decimal(remainder / NumberStep)
                    while i < integer_part and self.Check == 1:
                            i=i+1
                            self.master.update()
                            print(f"\nPosition axe 2 vérif :: '{axis2.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                            axis2.move_relative(NumberStep, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                            
                            if self.Check==1 and abs((self.Limit_MaxAxis2+Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))))>0.3 :    
                                axis2.move_absolute(self.Limit_MaxAxis2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                      
                            if self.Check==2:
                                    self.stop_all_axis()
                                    break
                                    
                            
            number50 = axis1.get_position(Units.LENGTH_MILLIMETRES)
            number150 = axis2.get_position(Units.LENGTH_MILLIMETRES)    
            print(f"\nPosition axe 1 :: '{number50}'")
            print(f"\nPosition axe 2 :: '{number150}'")
            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
            self.master.update()
                            
                            
                            
            
        def decrease (self, button_num):
            number50 = Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))
            number150 = Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES))
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
                            self.stop_all_axis()
                            break
            elif button_num == 2:

                    while i < 20 and self.Check == 1:
                        i=i+1
                        self.master.update()
                        print(f"\nPosition axe 1 vérif :: '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'\n")
                        axis2.move_relative(-0.5, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                        self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                        self.master.update()
                        if self.Check==2:
                                self.stop_all_axis()
                                break
            number50 = axis1.get_position(Units.LENGTH_MILLIMETRES)
            number150 = axis2.get_position(Units.LENGTH_MILLIMETRES)    
            print(f"\nPosition axe 1 :: '{number50}'")
            print(f"\nPosition axe 2 :: '{number150}'")
            
        
                    
        '''
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
        '''
        
        def stop_all_axis(self):
            self.change_color(1)
            try:
                if self.Check==1:
                    axis1.stop(wait_until_idle = True)
                    axis2.stop(wait_until_idle = True)
                    device.all_axes.stop()
                    self.Check=2
                    self.master.update()
                    self.master.update()
                    print(f"\nStop : '{self.Check}'")
                    
                if self.Check==2:
                    device.all_axes.stop()
                self.change_color(1)
            except AttributeError:
                # Axe non initialisé
                pass
            
            
        def StopAxis(self, num):
            if num==1:
                try:
                    if self.Check==1:
                        axis1.stop(wait_until_idle = True)
                        self.master.update()
                        self.Check=2
                        self.master.update()
                        print(f"\nStop : '{self.Check}'")
                    if self.Check==2:
                        device.all_axes.stop()
                except AttributeError:
                    # Axe non initialisé
                    pass       
            elif num==2:
                try:
                    if self.Check==1:
                        axis2.stop(wait_until_idle = True)
                        self.master.update()
                        self.Check=2
                        self.master.update()
                        print(f"\nStop : '{self.Check}'")
                    if self.Check==2:
                        device.all_axes.stop()
                except AttributeError:
                    # Axe non initialisé
                    pass  
            self.change_color(1)
                
        def TwoDevice(self, numberselection):
            increment_value = Decimal("0.00000001")
            number=0.654
            value=0
            if numberselection==1:
                if "." in self.number_text_AbsolutePosition.get():
                    a=0
                else:
                    value=Decimal(self.number_text_AbsolutePosition.get())
                print(f"\n value : '{value}'")
                #value = float(value)
                MovementTime = Decimal('16.00000000')/Decimal('2')
                print(f"\n axis1.get_position(Units.LENGTH_MILLIMETRES) : '{axis1.get_position(Units.LENGTH_MILLIMETRES)}'")
                random_number_step=Decimal(0.075)
                print(f"\n MovementTime : '{MovementTime}'")
                TimeByStep=(abs(random_number_step)*MovementTime)/(abs(Decimal(str(axis1.get_position(Units.LENGTH_MILLIMETRES))) - value)+1)
                velocity0= random_number_step/TimeByStep
                quotient, remainder = divmod(abs(value-axis1.get_position(Units.LENGTH_MILLIMETRES)+increment_value), random_number_step)
                integer_part = quotient-1
                decimal_part = remainder / random_number_step
                
                random_number_step2 = (abs(value-Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))))/quotient   
                                 
                quotient2, remainder = divmod(abs(value-Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))+increment_value), random_number_step2)
                integer_part2 = quotient2-1
                decimal_part2 = remainder / random_number_step2     
                
                if axis1.get_position(Units.LENGTH_MILLIMETRES) < value and axis2.get_position(Units.LENGTH_MILLIMETRES) < value :
                            #à envoyer : MovementTime, integer_part,decimal_part, random_number_step, la velocité nommé velocity0, ConfigureNumber (dans quel "if" on est), 
                    self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, value, value, velocity0, 1)
                          
                elif axis1.get_position(Units.LENGTH_MILLIMETRES) > value and axis2.get_position(Units.LENGTH_MILLIMETRES) < value :
                    self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, value, value, velocity0, 2)
                elif axis1.get_position(Units.LENGTH_MILLIMETRES) < value and axis2.get_position(Units.LENGTH_MILLIMETRES) > value :
                    self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, value, value, velocity0, 3)
                elif axis1.get_position(Units.LENGTH_MILLIMETRES) > value and axis2.get_position(Units.LENGTH_MILLIMETRES) > value :    
                    self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, value, value, velocity0, 4)
                          
            elif numberselection==2:
                    if "." in self.number_text_RelativePosition.get():
                        a=0
                    else:
                        value=Decimal(self.number_text_RelativePosition.get() + ".000")
                    while axis1.get_position(Units.LENGTH_MILLIMETRES) < self.Limit_MaxAxis1 or axis2.get_position(Units.LENGTH_MILLIMETRES) < self.Limit_MaxAxis2 and self.Check == 1:
                            
                            i=0
                            j=0
                                                   
                            while axis1.get_position(Units.LENGTH_MILLIMETRES) < self.Limit_MaxAxis1 and i==0 and self.Check == 1:
                                i=i+1
                                axis1.move_relative(value, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                                
                            while axis2.get_position(Units.LENGTH_MILLIMETRES) < self.Limit_MaxAxis2 and i==1 and self.Check == 1:
                                axis2.move_relative(value, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                                j=i+1
                            
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                            if self.Check==2:
                                    self.stop_all_axis()
                                    break
            elif numberselection==3:
                    if "." in self.number_text_RelativePosition.get():
                        a=0
                    else:
                        value=Decimal(self.number_text_RelativePosition.get() + ".000")
                    while self.Check == 1:
                            
                            i=0
                            j=0
                            self.master.update()                            
                            while i==0 and axis1.get_position(Units.LENGTH_MILLIMETRES) > self.Limit_MinAxis1 and self.Check == 1:
                                i=i+1
                                axis1.move_relative(-value, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                            while axis2.get_position(Units.LENGTH_MILLIMETRES) > self.Limit_MinAxis2 and j==0 and self.Check == 1:
                                axis2.move_relative(-value, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                                j=i+1
                            
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                            if self.Check==2:
                                self.stop_all_axis()
                                break
            elif numberselection==4:
                    if "." in self.number_text_RelativePosition.get():
                        a=0
                    else:
                        value=Decimal(self.number_text_RelativePosition.get() + ".000")
                    while axis1.get_position(Units.LENGTH_MILLIMETRES) < self.Limit_MaxAxis1 or axis2.get_position(Units.LENGTH_MILLIMETRES) < self.Limit_MaxAxis2 and self.Check == 1:
                            
                            i=0
                            j=0
                                                   
                            while axis1.get_position(Units.LENGTH_MILLIMETRES) < self.Limit_MaxAxis1 and i==0 and self.Check == 1:
                                i=i+1
                                axis1.move_relative(number, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = value, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                                
                            while axis2.get_position(Units.LENGTH_MILLIMETRES) < self.Limit_MaxAxis2 and j==0 and self.Check == 1:
                                axis2.move_relative((number/3), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = value/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                                j=j+1
                            
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                            if self.Check==2:
                                self.stop_all_axis()
                                break
            elif numberselection==5:
                    if "." in self.number_text_RelativePosition.get():
                        a=0
                    else:
                        value=Decimal(self.number_text_RelativePosition.get() + ".000")
                   
                    while axis1.get_position(Units.LENGTH_MILLIMETRES) > self.Limit_MinAxis1 or axis2.get_position(Units.LENGTH_MILLIMETRES) > self.Limit_MinAxis2 and self.Check == 1:
                            
                            i=0
                            j=0
                            self.master.update()
                            while i==0 and axis1.get_position(Units.LENGTH_MILLIMETRES) > self.Limit_MinAxis1 and self.Check == 1:
                                i=i+1
                                axis1.move_relative(-number, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = value, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                            while axis2.get_position(Units.LENGTH_MILLIMETRES) > self.Limit_MinAxis2 and j==0 and self.Check == 1:
                                axis2.move_relative(-(number/3), unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = value/3, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                                j=i+1
                            
                            self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                            self.master.update()
                            if self.Check==2:
                                self.stop_all_axis()
                                break
                
                
        def update_labels(self, new_number150, new_number50):
            self.number150_str.set(str(new_number150))
            self.number50_str.set(str(new_number50))
            self.master.update()
    
        def Check1to2(self):
            self.Check = 1
            print(f"\n Check : '{self.Check}'")
            self.change_color(2)
            
        def change_color(self, num):
            if num==1:
                if self.case["bg"] == "green":
                    self.case.config(bg="red")
            elif num==2:
                self.case.config(bg="green")
                
        def circle(self):

            # Créer une nouvelle fenêtre
            window = tk.Toplevel()
            self.positionAxis1circle = {}
            self.positionAxis2circle = {}
            self.MovementTimecircle = {}
            self.Diameter = {}
            label = ttk.Label(window, text="Movement linear").grid(row=1, column=1, columnspan=2)
            label = ttk.Label(window, text="Position Axis1 (in mm) :").grid(row=2, column=1)
            self.PositionAxis1circle = ttk.Entry(window)
            self.PositionAxis1circle.grid(row=2, column=2)
            
            label = ttk.Label(window, text="Position Axis2 (in mm) :").grid(row=3, column=1)
            self.PositionAxis2circle = ttk.Entry(window)
            self.PositionAxis2circle.grid(row=3, column=2)
            
            label = ttk.Label(window, text="Mouvement time (in s) :").grid(row=4, column=1)
            self.MovementTimecircle = ttk.Entry(window)
            self.MovementTimecircle.grid(row=4, column=2)
            
            label = ttk.Label(window, text=" ").grid(row=5, column=1)
            
            label = ttk.Label(window, text="Diameter (in mm) :").grid(row=6, column=1)
            self.Diameter = ttk.Entry(window)
            self.Diameter.grid(row=6, column=2)            
            label = ttk.Label(window, text=" ").grid(row=7, column=1)
            
            
            label = ttk.Label(window, text="How many loop :").grid(row=8, column=1)
            self.LoopCircle = ttk.Entry(window)
            self.LoopCircle.grid(row=8, column=2)            
            label = ttk.Label(window, text=" ").grid(row=9, column=1)
            
            
            
            self.ACCEPT_ALL = ttk.Button(window, text="ACCEPT ALL", width=15, command=lambda:self.circleMovement(self.PositionAxis1circle, self.PositionAxis2circle, self.MovementTimecircle, self.Diameter))
            self.ACCEPT_ALL.grid(row=11, column=2) 


        def circleMovement(self, PositionAxis1circle, PositionAxis2circle, MovementTimecircle, Diameter):
                
                increase = Decimal(0.00000001)
                increase2=Decimal(1.0000000)
                if self.LoopCircle.get()!='':
                    self.LoopCircle = int(LoopCircle.get())
                else:
                    self.LoopCircle = 1

                print(f"\n LoopCircle : {self.LoopCircle}")
                if "." in str(Diameter):
                    a=0
                else:
                        Diameter=Decimal(self.Diameter.get() + ".000")
                if PositionAxis1circle.get() !="":
                    self.PositionAxis1circle = Decimal(PositionAxis1circle.get())
                else:
                    self.PositionAxis1circle= Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES))
                if PositionAxis2circle.get() !="":
                    self.PositionAxis2circle = Decimal(PositionAxis2circle.get())
                else:
                    self.PositionAxis2circle= Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))
                
                MovementTime = Decimal(20/2)
                if abs(self.PositionAxis1circle-Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES)))<0.5 or abs(self.PositionAxis2circle-Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES)))<0.5:
                    MovementTime = Decimal(6/2)
                
                random_number_step=Decimal(0.0150000)
                
                TimeByStep=(abs(random_number_step)*MovementTime)/(abs(Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES)) - self.PositionAxis1circle)+increase2)         
                velocity0= random_number_step/TimeByStep
                quotient, remainder = divmod(abs(self.PositionAxis1circle-Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES))+increase), random_number_step)
                integer_part = quotient-1
                decimal_part = Decimal(remainder / random_number_step)
                
                print(f"\n decimal part : {decimal_part}")
                if quotient !=0:
                    random_number_step2 = (abs(self.PositionAxis2circle-Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))))/quotient   
                else:
                    random_number_step2 = (abs(self.PositionAxis2circle-Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))))/1
                
                if axis1.get_position(Units.LENGTH_MILLIMETRES) < self.PositionAxis1circle and axis2.get_position(Units.LENGTH_MILLIMETRES) < self.PositionAxis2circle :
                            #à envoyer : MovementTime, integer_part,decimal_part, random_number_step, la velocité nommé velocity0, ConfigureNumber (dans quel "if" on est), 
                    self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, self.PositionAxis1circle, self.PositionAxis2circle, velocity0, 1)
                elif axis1.get_position(Units.LENGTH_MILLIMETRES) > self.PositionAxis1circle and axis2.get_position(Units.LENGTH_MILLIMETRES) < self.PositionAxis2circle :
                    self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, self.PositionAxis1circle, self.PositionAxis2circle, velocity0, 2)
                elif axis1.get_position(Units.LENGTH_MILLIMETRES) < self.PositionAxis1circle and axis2.get_position(Units.LENGTH_MILLIMETRES) > self.PositionAxis2circle :
                    self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, self.PositionAxis1circle, self.PositionAxis2circle, velocity0, 3)
                elif axis1.get_position(Units.LENGTH_MILLIMETRES) > self.PositionAxis1circle and axis2.get_position(Units.LENGTH_MILLIMETRES) > self.PositionAxis2circle :    
                    self.mouvement_Move_Plate(MovementTime, integer_part, decimal_part, random_number_step, random_number_step2, self.PositionAxis1circle, self.PositionAxis2circle, velocity0, 4)
                  
                self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES))
                
                OldPositionAxis1=Decimal(axis1.get_position(Units.LENGTH_MILLIMETRES))
                OldPositionAxis2=Decimal(axis2.get_position(Units.LENGTH_MILLIMETRES))
                i=0
            
                while i<self.LoopCircle and self.Check == 1:
                    j=0
                    
                    
                    
                    x=0
                    y=0
                    diameter = self.Diameter
                    rayon=diameter/2
                    centre_x = 0
                    centre_y = 0
                    nb_etapes = 16
                    angle_step = 2 * math.pi / nb_etapes
                    y1=0
                    x1=0
                    while j<nb_etapes and self.Check == 1:
                    # Calculer l'angle de cette étape
                        angle = j * angle_step
                
                        
                        

                        # Calculer les coordonnées de cette étape
                        x = -(centre_x + rayon * math.cos(angle))
                        y = (centre_y + rayon * math.sin(angle))
                        # Afficher les coordonnées de cette étape
                        print("Étape", j+1, ": (", x, ",", y, ")")
    
                        if x<0.001:
                                x=0
                            
                        if self.Check==2:
                                self.stop_all_axis()
                                break
                        nb_1etapes=nb_etapes/2
                    
                        
                        axis1.move_relative(abs(x-rayon)-x1, wait_until_idle = True, velocity = 0.5, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                        if self.Check==2:
                                self.stop_all_axis()
                                break
                        
                        axis2.move_relative(y-y1, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0.5, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                                    
                        
                        if self.Check==2:
                                self.stop_all_axis()
                                break
                        # Afficher les coordonnées de cette étape
                        j=j+1
                        if self.Check==2:
                                self.stop_all_axis()
                                break
                        print("Etape réel ", j+1, ": (", axis1.get_position(Units.LENGTH_MILLIMETRES), ",", axis2.get_position(Units.LENGTH_MILLIMETRES), ")\n")
                        self.update_labels(axis1.get_position(Units.LENGTH_MILLIMETRES), axis2.get_position(Units.LENGTH_MILLIMETRES)) 
                        x1=x
                        y1=y
                        
                    i=i+1
                    if self.Check==2:
                        self.stop_all_axis()
                        break
                axis1.move_relative(OldPositionAxis1, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0.5, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
                axis2.move_relative(OldPositionAxis2, unit = Units.LENGTH_MILLIMETRES, wait_until_idle = True, velocity = 0.5, velocity_unit = Units.VELOCITY_MILLIMETRES_PER_SECOND, acceleration = 0, acceleration_unit = Units.NATIVE)
            
            # Créer une nouvelle fenêtre
                           
                #self.TwoDevice(1)
            
    # Démarrage de la boucle principale
    root = tk.Tk()
    interface = Interface(root)
    
    root.mainloop()
