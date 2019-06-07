#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial



class chassis(object):

    def __init__(self):
        self.ser = serial.Serial("/dev/tty.HC-06-DevB", 9600, timeout=0.5)
        # self.ser = None
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


    def close(self):
        self.ser.close()