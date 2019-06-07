#!/usr/bin/python3
# -*- coding: utf-8 -*-


import cv2
import numpy as np

def RGB2BW(src, blockSize):
    img_gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    img_thres = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, 6)
    return img_thres

def regulateImg(src, srcPoints, targetPoints):
    M = cv2.getPerspectiveTransform(srcPoints, targetPoints)
    img_regulate = cv2.warpPerspective(src, M, (720, 720))
    return img_regulate

def filter_out_RB(src):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([110, 100, 100])    # 后面两个值可以动
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(hsv, hsv, mask = mask_blue)

    lower_red = np.array([-10, 210, 210])
    upper_red = np.array([10, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    res_red = cv2.bitwise_and(hsv, hsv, mask = mask_red)


    cv2.imshow("res_red_filter", res_red)
    cv2.imshow("res_blue_filter", res_blue)
    cv2.imshow("src", src)
    cv2.waitKey()

    return res_red, res_blue

