#!/usr/bin/python3
# -*- coding: utf-8 -*-

import img_tools
import cv2

res_red, res_blue = img_tools.filter_out_RB(gv.test_img)
cv2.imshow("OR", cv2.bitwise_or(res_red, res_blue))


term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
track_window = ()
ret, trackWindow = cv2.CamShift(res_red, track_window, term_crit)



#cv2.imshow("filter", res)
cv2.waitKey(0)