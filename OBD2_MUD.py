#Definicoes de endereços dos sensores e conversoes necessarias 
SPEED = 'A02F'
COOLANT_TEMP = 'A007'
COOLANT_TEMP_SCALED = 'A010'
EGR_TEMP = 'A012'
BATERY_VOLTAGE = 'A014'
BAROMETER = 'A015'
THROTTLE_POSITION = 'A017'
ENGINE_RPM = 'A021'
ACEL_LOAD = 'A056'

def Get_SpeedKPH(response):
    l, r = response[:8], response[8:]
    val = int(r[:2], 16)
    speed = int((val * 1.2427424) * 1.609344)
    return speed

def Get_SpeedKPM(response):
    l, r = response[:4], response[4:]
    val = int(l[2:], 16)
    speed = int(val * 1.2427424)
    return speed

def Get_Coolant_Temp_C(response):
    l, r = response[:8], response[8:]
    val = int(r[:2], 16)
    cool = int((val*1.8)/0.555)
    return cool
def Get_Coolant_Temp_F(response):
    l, r = response[:8], response[8:]
    val = int(r[:3], 16)
    cool = int((val*1.8) +32)
    return cool
    
def Get_Coolant_Temp_Scaled_C(response):
    l, r = response[:8], response[8:]
    val = int(r[:3], 16)
    cool = int((((val*1.8)-40)-32)/0.555)
    return cool
def Get_Coolant_Temp_Scaled_F(response):
    l, r = response[:8], response[8:]
    val = int(r[:3], 16)
    cool = int((val*1.8)-40)
    return cool

def Get_EGR_temp_C(response):
    l, r = response[:8], response[8:]
    val = int(r[:3], 16)
    egr = ((-2.7 * val + 597.7)-32)/0.555
    return egr     
def Get_EGR_temp_F(response):
    l, r = response[:8], response[8:]
    val = int(r[:3], 16)
    egr = (-2.7 * val + 597.7)
    return egr 

def Get_Batery_Voltage(response):
    l, r = response[:8], response[8:]
    val = int(r[:2], 16)
    bat = val * 0.07333
    #if(bat > 20): bat = 0
    return bat

def Get_Barometer(response):
    l, r = response[:8], response[8:]
    val = int(r[:3], 16)
    baro = val * 0.49
    return baro

def Get_RPM(response):
    l, r = response[:4], response[4:]
    val = int(l[2:], 16)
    rpm = int(val * 31.25)
    return rpm

    
def Get_Acel_Load(response):
    l, r = response[:8], response[8:]
    val = int(r[:3], 16)
    acel = (val*100)/255
    return acel

def Get_Throttle_pos(response):
    l, r = response[:8], response[8:]
    val = int(r[:3], 16)
    throttle = (val * 100)/255
    return throttle
                