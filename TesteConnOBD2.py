import serial
import time
import string
import io
import os
import sys

ser = serial.Serial("/dev/rfcomm9")
ser.baudrate = 10400
s = input('Enter AT command --> ')
print ('AT command = ' + s)
ser.flushInput();
ser.write(bytes(s + '\r\n', encoding = 'utf-8'))
ser.flush();
ser.timeout = 1
response = ser.read(999).decode('utf-8')
print(response)
ser.close()