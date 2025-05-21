import serial

ser = None
try:
    #ser = serial.Serial(port='COM5', baudrate=115200, timeout=0.1) # Windows
    ser = serial.Serial(port="/dev/ttyAPE0",baudrate=115200,timeout=0.1) # raspberry pi
    print("Found Micro:Bit")
    
except:
    print("Not Found Micro:bit")
while True:
    if ser.in_waiting:
        command = ser.readline().decode().strip()

    print(command)
