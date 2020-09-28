#!/bin/bash
sudo modprobe w1-gpio
sudo modprobe w1-therm
sudo ./RTC_DS1302-master/PythonRTC.py
python3 ./Clock_092020.py
