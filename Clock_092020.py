#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tkinter as tk
import locale , requests
from   PIL    import Image, ImageTk, ImageDraw
import time
import numpy as np
import os
import socket
import glob
import string
import io
import sys
import serial
import OBD2_MUD as MUD

#inicializa comunicacao com arduino via usb
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#inicializa comunicacao com obd2
os.system('lxterminal -e /home/pi/Documents/bootOBD2')

s = [0,1]
ser = 0

color_temp = 'white'
color_mot = 'white'
color_gas = 'white'
color_vel = 'white'
color_bat = 'white'

#Conecta com obd2 (atencao ao numero do rfcomm que vc configurar)
def OBDConn():
    global obd
    time.sleep(1)
    obd = serial.Serial("/dev/rfcomm9")
    obd.baudrate = 38400
    if obd.inWaiting() > 0:
        obd.flushInput()
    #obd.timeout = 1.

#Pega os dados de velocidade e faz a conversao necessaria 
def GetVelocity():    
    obd.write(bytes(MUD.SPEED + '\r\n', encoding = 'utf-8'))
    obd.flush();
    obd.timeout = 1
    response = obd.read(999).decode('utf-8')
    #print(response)
    vel = MUD.Get_SpeedKPH(response)
    if(vel>300): vel =0    
    return vel
#Pega os dados de temperatura de arrefecimento e faz a conversao necessaria 
def GetMotorTemp():
    if obd.inWaiting() > 0:
        obd.flushInput()
    obd.write(bytes(MUD.COOLANT_TEMP + '\r\n', encoding = 'utf-8'))
    obd.flush();
    obd.timeout = 1
    response = obd.read(999).decode('utf-8')
    motor = MUD.Get_Coolant_Temp_C(response)
    if(motor > 200):motor=0
    return motor
#Pega os dados de bateria
def GetBattery():
    if obd.inWaiting() > 0:
        obd.flushInput()
    obd.write(bytes(MUD.BATERY_VOLTAGE + '\r\n', encoding = 'utf-8'))
    obd.flush();
    obd.timeout = 1
    response = obd.read(999).decode('utf-8')
    bat = MUD.Get_Batery_Voltage(response)
    if(bat > 15):bat=0
    return bat

#Pega o nivel de combustivel via arduino
def update_fuel():
    ser = serial.Serial()
    ser.close()
    ser = serial.Serial('/dev/ttyUSB0',9600)
    read_serial=ser.readline()
    s[0] = int(ser.readline(),16)
    ser.close()
    gasOhm = s[0]
    if(gasOhm <= 10):gas = 100
    if(gasOhm > 10):gas = 110 - gasOhm
    return gas

#Pega temperatura do sonsor 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


locales = ['pt_BR.utf-8']
for loc in locales:
    locale.setlocale(locale.LC_ALL, loc)
root = tk.Tk()
root.attributes("-fullscreen", True) 

#Carrega a imagem de fundo
image=ImageTk.PhotoImage(Image.open("//home//pi//Documents//mitr4tran_092020.png"))

#Grupo de cores que irão variar
color = ["white", "misty rose", "gray", "cornflower blue", "medium blue",
         "light sky blue", "cyan", "lime green", "gold", 'indian red','salmon','tomato', 'pale violet red'
        , 'light pink','dark orchid', 'SlateBlue1', 'LightBlue1']
cnt = 0
colour = 'white'
#Gera background
canvas = tk.Canvas(root,width=480,height=320,bd=0, highlightthickness=0,background=colour)

#Posicionamento da imagem e palavras
canvas.create_image(0,0,anchor='nw',image=image)

clock_datetime = canvas.create_text(100, 45, fill="white", font=("arial", 60, "bold"),anchor='center')
clock_second = canvas.create_text(220, 30, fill="white", font=("arial", 22, "bold"),anchor='center')

clock_motor = canvas.create_text(80, 270, fill=color[0], font=("arial", 18, "bold"),anchor='center')
clock_batery = canvas.create_text(80, 200, fill=color[0], font=("arial", 18, "bold"),anchor='center')

clock_temperature = canvas.create_text(250, 80, fill=color[0], font=("arial", 21, "bold"),anchor='center')
clock_tank = canvas.create_text(395, 80, fill=color[0], font=("arial", 21, "bold"),anchor='center')

clock_kmh = canvas.create_text(275, 200, fill=color[0], font=("arial", 110, "bold"),anchor='center')
clock_kmh_unit = canvas.create_text(420, 245, fill=color[0], font=("arial", 18, "bold"),anchor='center')

clock_date = canvas.create_text(180, 300, fill=color[0], font=("arial", 20, 'bold'),anchor='center')
clock_dateweek = canvas.create_text(300, 300, fill=color[0], font=("arial", 20, 'bold'),anchor='center')

canvas.pack()

#Inicializando
mot = 0
gas = 0
vel = 0
gasPercent= "%"
temperatura = 0    
gasOhm = 0
bat = 0

temperatura = read_temp() #Temperatura pelo sensor acoplado no Raspberry
gas = update_fuel() #Nivel do tanque pelo arduino
OBDConn()
mot = GetMotorTemp() #Temperatura pelo OBD2
bat = GetBattery()
battery = "%.1fV"  % (bat)
temperaturas = "%.0f°C"  % (temperatura)
week = "%s" % (time.strftime('%d/%m/%Y'))
date = "%s" % (time.strftime('%A').title())
if(mot > 95):
    color_mot = color[10]
if(gas < 25):
    color_gas = color[10]
if(temperatura > 35):
    color_temp = color[10]
         
motor = "%s°C" % mot            
canvas.itemconfigure(clock_date, text=date, fill=colour)
canvas.itemconfigure(clock_dateweek, text=week, fill=colour)
canvas.itemconfigure(clock_temperature, text=temperaturas, fill=color_temp)
canvas.itemconfigure(clock_motor, text=motor, fill=color_mot)
canvas.itemconfigure(clock_batery, text=battery, fill=color_mot)
        
#Faz a troca da cor e a leitura da temperatura interna a cada minuto no segundo 1,
#a cada 10 minutos atualiza a temperatura do motor e nivel de tanque
def getcolor():
    if (int(time.strftime('%S')) == 1):
        if (int(time.strftime('%M'))%1) == 0:
            global cnt 
            cnt+=1
            if cnt > 16:
                cnt = 0
            colour = color[cnt] 
            canvas.configure(background=colour)
            temperatura = read_temp()
            temperaturas = "%.0f°C"  % (temperatura)
            color_temp = color[3] 
            if(temperatura > 35):
                color_temp = color[10]
            canvas.itemconfigure(clock_temperature, text=temperaturas, fill=color_temp)
        if (int(time.strftime('%M'))%10) == 0:
            mot = GetMotorTemp()        
            if(mot > 95):
                color_mot = color[10]
            motor = "%s°C" % mot            
            color_mot = color[3]
            canvas.itemconfigure(clock_motor, text=motor, fill=color_mot)
      
            week = "%s" % (time.strftime('%d/%m/%Y'))
            date = "%s" % (time.strftime('%A').title())
            color_mot = 'white'
            color_gas = 'white'
            color_temp = 'white'
            gas = update_fuel()
            if(gas < 25):
                color_gas = color[10]
            canvas.itemconfigure(clock_date, text=date, fill=colour)
            canvas.itemconfigure(clock_dateweek, text=week, fill=colour)
                               
def update():
    try:
        velocidade = GetVelocity()
        colour = color[cnt]        
        color_temp = color[3]
        color_gas = color[0]
        color_vel = color[0]
        if(vel > 60):
            color_vel = color[8]
        if(vel > 80):
            color_vel = color[10]
        hora = time.strftime('%H:%M') # local
        segundo = time.strftime('.%S') # local
        
        
        percent = "%"
        fuel = "%s%s " % (gas,percent )       
        
        canvas.itemconfigure(clock_datetime, text=hora)
        canvas.itemconfigure(clock_second, text=segundo)
        canvas.itemconfigure(clock_tank, text=fuel, fill=color_gas)
        canvas.itemconfigure(clock_kmh, text=velocidade, fill=color_vel)
        canvas.itemconfigure(clock_kmh_unit, text="Km/h", fill=colour)
        canvas.update()
        getcolor()
        root.after(10, update)
        
    except StopIteration:
        pass

update()
root.mainloop()


# In[ ]:



