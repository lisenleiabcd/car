#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import img_tools
import numpy as np
from car_detect import car_dectect
from find_path import bfs
from matplotlib import pyplot as plt
import time

thresholdVal = 0
IMG_SIZE = 720


targetPoints = np.float32([[0, 0],
                         [IMG_SIZE, 0],
                         [IMG_SIZE, IMG_SIZE],
                         [0, IMG_SIZE]])
srcPoints = np.float32([[0, 0], [0, 0], [0, 0], [0, 0]])
BLKSIZE = [2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 20, 24, 30, 32, 36, 40, 45, 48, 50, 60, 72, 80, 90, 120]
NUM_BLKSIZE_CHOICE = 25

global nextSrcPtIndex
nextSrcPtIndex = 0
global mapSize
mapSize = 10
blockSize = 0
bw_arg = 0;
map = []
img_virtual = np.ones((IMG_SIZE, IMG_SIZE), np.uint8)
mapGenerated = False
desIJ = (-1, -1)

def xy2ij(x, y):
    return int(y / blockSize), int(x / blockSize)


def setFilter():
    global bw_arg
    while (1):
        bw_arg = cv2.getTrackbarPos("BW_blk_size", "image")
        img_BW = img_tools.RGB2BW(img_regulate, 2 * bw_arg + 3)
        cv2.imshow("image", img_BW)
        k = cv2.waitKey(1000) & 0xFF
        if k == 32:
            break
    return img_BW

def generateMap(img_BW):
    global mapSize
    global blockSize
    prevChoice = -1
    while(1):

        choice = cv2.getTrackbarPos("map_blk_size", "image")
        if (prevChoice != choice):
            blockSize = BLKSIZE[choice]
            mapSize = int(IMG_SIZE / blockSize)                # 必须是正方形，整块划分
            map.clear()

            for j in range(0, mapSize):
                map.append([])
                for i in range(0, mapSize):
                    (mean, stddv) = cv2.meanStdDev(img_BW[j * blockSize : (j + 1) * blockSize \
                                                    , i * blockSize : (i + 1) * blockSize])
                    #cv2.imshow("test", img_BW[j * block_size : (j + 1) * block_size \
                    #                                , i * block_size : (i + 1) * block_size])

                    if (mean > 200):          ########valve value!!!!!!!!!!
                        map[j].append(255)
                        img_virtual[j * blockSize: (j + 1) * blockSize \
                            , i * blockSize: (i + 1) * blockSize] = 255;
                    else:
                        map[j].append(0)
                        img_virtual[j * blockSize: (j + 1) * blockSize \
                            , i * blockSize: (i + 1) * blockSize] = 0;


            cv2.imshow("img_virtual", img_virtual)

        prevChoice = choice
        k = cv2.waitKey(1000) & 0xFF
        if k == 32:
            break







def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global nextSrcPtIndex
    global mapGenerated
    global desIJ
    if event == cv2.EVENT_LBUTTONDOWN:
        if (nextSrcPtIndex >= 4):
            if (mapGenerated):
                i, j = xy2ij(x, y)
                desIJ = (i, j)
                img_virtual[i * blockSize: (i + 1) * blockSize \
                    , j * blockSize: (j + 1) * blockSize] = 150;
                map[i][j] = 255
                cv2.imshow("img_virtual", img_virtual)
                mapGenerated = False

            else:
                pass
        else:
            cv2.circle(img_test, (x, y), 1, (255, 0, 0), thickness=-1)
            srcPoints[nextSrcPtIndex, 0] = x;
            srcPoints[nextSrcPtIndex, 1] = y;
            nextSrcPtIndex = nextSrcPtIndex + 1
            cv2.imshow("image", img_test)

############################################################ begin!!!!!!!!!!!!!!

cv2.namedWindow("image")
#cap = cv2.VideoCapture(0)
# take first frame of the video
'''
while (1):
    ret, img_test = cap.read()
    k = cv2.waitKey(1000) & 0xFF
    if k == 32:
        break
  '''

img_test = cv2.imread("testPic.png")
cv2.imshow("image", img_test)

cv2.imshow("image", img_test)
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.createTrackbar('BW_blk_size', 'image', 0, int(IMG_SIZE / 2 - 1), lambda x: None)
cv2.createTrackbar('map_blk_size', 'image', 15, NUM_BLKSIZE_CHOICE - 1, lambda x: None)


cv2.waitKey(0)
img_regulate = img_tools.regulateImg(img_test, srcPoints, targetPoints)
cv2.imshow("image_regulate", img_regulate)

img_BW = setFilter()
cv2.destroyWindow("image_regulate")
generateMap(img_BW)
mapGenerated = True
#标定终点
cv2.setMouseCallback("img_virtual", on_EVENT_LBUTTONDOWN)
cv2.waitKey(0)
#
print("put the car!!!!!!!!!!!!!!")
cv2.waitKey(0)
routine = np.empty((mapSize, mapSize), dtype=tuple)

while (1):
    #ret, img = cap.read()
    img = cv2.imread("testPic.png")

    img_regulate = img_tools.regulateImg(img, srcPoints, targetPoints)
    head_coords, tail_coords = car_dectect(img_regulate)
    car_center = ((head_coords[0] + tail_coords[0]) / 2, (head_coords[1] + tail_coords[1]) / 2)
    curIJ = xy2ij(car_center[0], car_center[1])
    if (routine[curIJ[0]][curIJ[1]] is None):           #不在路径中，寻路
        routine = bfs(map, mapSize, desIJ, curIJ)
        print("here")
        tmp = curIJ
        # draw the routine########################################3
        while (1):
            img_virtual[tmp[0] * blockSize: (tmp[0] + 1) * blockSize \
                , tmp[1] * blockSize: (tmp[1] + 1) * blockSize] = 70;
            tmp = routine[tmp[0]][tmp[1]]
            if (tmp == desIJ):
                break;
        print("@#@#@#@#")
        cv2.imshow("image_virtual", img_virtual)
        cv2.waitKey(0)
        #######################################
    else:               #在路径中
        #ToDo
        pass

