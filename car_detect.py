#!/usr/bin/python3
# -*- coding: utf-8 -*-

import img_tools
import cv2
import numpy as np
import imutils
track_window_red = (0, 0, 720, 720)
track_window_blue = (0, 0, 720, 720)

def find_center(img_filtered):
    cnts = cv2.findContours(img_filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    for c in cnts:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    return cX, cY



def car_dectect(img_regulate):           #------> return coord(head), and coord(tail) in xy
    #global track_window_red
    #global track_window_blue
    img_red, img_blue = img_tools.filter_out_RB(img_regulate)

    ''' 
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    ret_red, track_window_red = cv2.CamShift(img_red, track_window_red, term_crit)
    ret_blue, track_window_blue = cv2.CamShift(img_blue, track_window_blue,term_crit)

    pts = cv2.boxPoints(ret_red)
    pts = np.int0(pts)

    img2 = cv2.polylines(img_regulate, [pts], True, 255, 2)
    cv2.imshow('Capture', img2)
    cv2.waitKey(0)
    '''

    return find_center(img_red), find_center(img_blue)




