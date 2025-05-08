import serial


ser = serial.Serial(port="COM5",baudrate=115200,timeout=0.1)
while True:

    command = ser.readline().decode().strip()

    print(command)
