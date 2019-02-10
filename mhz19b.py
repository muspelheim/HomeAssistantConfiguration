#!/usr/bin/env python
import serial
import time
import subprocess

class mhz19b():
    tty = 'ttyS0'
    measurement_range = "\xff\x01\x99\x00\x00\x00\x13\x88\xcb" # 0-5000ppi https://revspace.nl/MHZ19
    read_bytes = "\xff\x01\x86\x00\x00\x00\x00\x00\x79"
    stop_getty = 'sudo systemctl stop serial-getty@' + tty + '.service'
    start_getty = 'sudo systemctl start serial-getty@' + tty + '.service'

    def __init__(self, tty='ttyS0'):
        self.tty = tty
        self.init_measurement_range()

    def init_measurement_range(self):
        subprocess.call(self.stop_getty, stdout=subprocess.PIPE, shell=True)
        ser = serial.Serial('/dev/' + self.tty,
                            baudrate=9600,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=1.0)
        while 1:
            result = ser.write(self.measurement_range)
            s = ser.read(9)

            if s[0] == "\xff" and s[1] == "\x99" and s[2] == "\x01":
                print "Current measurement range is 0-5000";
                break

    def read_co2(self):
        try:
            subprocess.call(self.stop_getty, stdout=subprocess.PIPE, shell=True)
            ser = serial.Serial('/dev/' + self.tty,
                                baudrate=9600,
                                bytesize=serial.EIGHTBITS,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                timeout=1.0)
            while 1:
                result = ser.write(self.read_bytes)
                s = ser.read(9)
                if s[0] == "\xff" and s[1] == "\x86":
                    return {'co2': {"value": ord(s[2]) * 256 + ord(s[3]), 'unit': 'ppm', 'sensor': 'MH-Z19B'}}
                break
        except:
            return {}
            print ("failed to read co2 value. maybe lacks permission to read/write serial")
        finally:
            subprocess.call(self.start_getty, stdout=subprocess.PIPE, shell=True)

    def read_temperature(self):
        try:
            subprocess.call(self.stop_getty, stdout=subprocess.PIPE, shell=True)
            ser = serial.Serial('/dev/' + self.tty,
                                baudrate=9600,
                                bytesize=serial.EIGHTBITS,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                timeout=1.0)
            while 1:
                result = ser.write(self.read_bytes)
                s = ser.read(9)
                if s[0] == "\xff" and s[1] == "\x86":
                    return {'temp': {"value": ord(s[4]) - 40, 'unit': 'c', 'sensor': 'MH-Z19B'}}
                break
        except:
            return {}
            print ("failed to read co2 value. maybe lacks permission to read/write serial")
        finally:
            subprocess.call(self.start_getty, stdout=subprocess.PIPE, shell=True)

co2 = mhz19b()

while True:
    print co2.read_co2()
    print co2.read_temperature()
    time.sleep(5)