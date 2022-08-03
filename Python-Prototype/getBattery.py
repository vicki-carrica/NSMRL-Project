
import socket
import time
import keyboard
import math

HOST = "127.0.0.1"
PORT = 8423

#command = input("WHAT DO YOU WANT DA COMMAND TO SAY?")


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
    
print(GetBattery())

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
print(GetBatteryPlugged())


#data = data.decode('utf-8')
#print(data)
#if keyboard.is_pressed("q"):
   # print("no more battery info")
   # break
