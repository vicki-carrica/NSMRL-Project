
import socket
import math

#ip address and port of pisugar power manager api
HOST = "127.0.0.1"
PORT = 8423



#Gets Battery percentage from pisugar api, converts into float, and truncates decimals.
def GetBattery():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.sendall(bytes("get battery", 'utf-8'))
        data = s.recv(1024)
    data = data.decode('utf-8')
    data = data.replace("battery: ",'')
    data = data.replace("\n",'')
    data = float(data)
    data = math.trunc(data)
    return data 

#Returns True if battery is plugged into powersource, returns false if it isn't
def GetBatteryPlugged():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.sendall(bytes("get battery_power_plugged", 'utf-8'))
        data = s.recv(1024)
    data = data.decode('utf-8')
    data = data.replace("battery_power_plugged: ", '')
    data = data.replace("\n",'')
    if data == "true":
        return True
    else:
        return False 