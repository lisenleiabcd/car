#!/usr/bin/python3
# -*- coding: utf-8 -*-

import img_tools
import cv2
import numpy as np
import imutils
track_window_red = (0, 0, 720, 720)
track_window_blue = (0, 0, 720, 720)
img_red = cv2.imread("red2.png")
img_blue = cv2.imread("green2.png")

hsv_roi_red = cv2.cvtColor(img_red, cv2.COLOR_BGR2HSV)
mask_red = cv2.inRange(hsv_roi_red, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist_red = cv2.calcHist([hsv_roi_red], [0], mask_red, [180], [0, 180])
hsv_roi_blue = cv2.cvtColor(img_blue, cv2.COLOR_BGR2HSV)
mask_blue = cv2.inRange(hsv_roi_blue, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist_blue = cv2.calcHist([hsv_roi_blue], [0], mask_blue, [180], [0, 180])

def find_center(pts):
    return ((pts[0] + pts[1] + pts[2] + pts[3]) / 4).astype(int)


# car_dectect.....一开始拼错了后面就没改23333333
def car_dectect(img_regulate):           #------> return coord(head), and coord(tail) in xy


    hsv = cv2.cvtColor(img_regulate, cv2.COLOR_BGR2HSV)
    dst_hist_red = cv2.calcBackProject([hsv], [0], roi_hist_red, [0, 180], 1)
    dst_hist_blue = cv2.calcBackProject([hsv], [0], roi_hist_blue, [0, 180], 1)

    img_r, img_b = img_tools.filter_out_RB(img_regulate)
    
    result_red = cv2.bitwise_and(dst_hist_red, img_r)
    result_blue = cv2.bitwise_and(dst_hist_blue, img_b)
    
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    ret_red, track_window_red_ = cv2.CamShift(result_red, track_window_red, term_crit)
    ret_blue, track_window_blue_ = cv2.CamShift(result_blue, track_window_blue, term_crit)

    pts_red = cv2.boxPoints(ret_red)
    pts_blue = cv2.boxPoints(ret_blue)
    pts_red = np.int0(pts_red)
    pts_blue = np.int0(pts_blue)

    img2 = cv2.polylines(img_regulate, [pts_red], True, 255, 2)
    img3 = cv2.polylines(img_regulate, [pts_blue], True, 0, 2)
    cv2.imshow('Capture', img2)
    
    return find_center(pts_red), find_center(pts_blue)




