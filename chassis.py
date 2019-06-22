#!/usr/bin/python3
# -*- coding: utf-8 -*-

##############################################
#
#   小车串口通信模块
#
##############################################

import serial

class chassis(object):

    def __init__(self):
        #self.ser = serial.Serial("/dev/tty.HC-06-DevB", 9600, timeout=0.5)
        self.ser = serial.Serial("COM3", 9600, timeout = 0.5)
        self.timestep = 0.085
        self.minDuration = 0.01

    def right(self):
        cmd = "R"
        self.ser.write(cmd.encode())

    def left(self):
        cmd = "L"
        self.ser.write(cmd.encode())

    def stop(self):
        cmd = "P"
        self.ser.write(cmd.encode())

    def forward(self):
        cmd = "A"
        self.ser.write(cmd.encode())

    def close(self):
        self.ser.close()
