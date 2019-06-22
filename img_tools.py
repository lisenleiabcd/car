#!/usr/bin/python3
# -*- coding: utf-8 -*-


import cv2
import numpy as np

# 从彩色图变为黑白
def RGB2BW(src, blockSize):
    img_gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    img_thres = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, 6)
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
    #img_closing = cv2.morphologyEx(img_thres, cv2.MORPH_CLOSE, kernel)

    #kernel = np.ones((40, 40), np.uint8)
    #img_erosion = cv2.erode(img_thres, kernel)
    return img_thres

#  坐标变换，纠正视角
def regulateImg(src, srcPoints, targetPoints):
    M = cv2.getPerspectiveTransform(srcPoints, targetPoints)
    img_regulate = cv2.warpPerspective(src, M, (720, 720))
    return img_regulate

# 过滤出车头和车尾两种颜色
def filter_out_RB(src):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([40, 50, 100])    # 60, 24, 100, 95, 115, 160
    upper_blue = np.array([70, 255, 255])   #40, 50, 100, 70, 255, 255
    #50, 70, 80, 80, 255, 255   #160, 70, 80, 180, 255, 255   # 0
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(hsv, hsv, mask = mask_blue)

    lower_red1 = np.array([0, 80, 100])   #165, 24, 100, 180, 115, 175
    upper_red1 = np.array([20, 255, 255])   #0, 80, 100, 20 ,255, 255
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)

    '''
    lower_red2 = np.array([0, 70, 80])
    upper_red2 = np.array([10, 255, 255])
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    '''
    res_red = cv2.bitwise_and(hsv, hsv, mask = mask_red1)


    return cv2.cvtColor(res_red, cv2.COLOR_RGB2GRAY), cv2.cvtColor(res_blue, cv2.COLOR_RGB2GRAY)

