#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import chassis

client = chassis.chassis()
client.left()
time.sleep(0.9)
client.stop()
client.forward()
time.sleep(1)
client.stop()
'''
cv2.namedWindow("image")
cap = cv2.VideoCapture(1) 
cap.set(12, 200)
while (1):
    ret, img_test = cap.read()
    cv2.imshow("image", img_test)

    k = cv2.waitKey(1) & 0xFF
    if k == 32:
        break
cv2.imshow("image", img_test)
cv2.waitKey(0)
a = cap.get(12)
print(a)
'''
