#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import img_tools
import numpy as np
from matplotlib import pyplot as plt
import time

thresholdVal = 0
IMG_SIZE = 720

img_test = cv2.imread("myPic.jpeg")
cv2.namedWindow("image")
cv2.imshow("image", img_test)

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
map = []
img_virtual = np.ones((IMG_SIZE, IMG_SIZE), np.uint8)
mapGenerated = False
desIJ = []

def xy2ij(x, y):
    return int(x / blockSize), int(y / blockSize)


def setFilter():
    while (1):
        block_size = cv2.getTrackbarPos("BW_blk_size", "image")
        img_BW = img_tools.RGB2BW(img_regulate, 2 * block_size + 3)
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
    if event == cv2.EVENT_LBUTTONDOWN:
        if (nextSrcPtIndex >= 4):
            if (mapGenerated):
                i, j = xy2ij(x, y)
                desIJ.append(i)
                desIJ.append(j)
                img_virtual[j * blockSize: (j + 1) * blockSize \
                    , i * blockSize: (i + 1) * blockSize] = 127;
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

cv2.imshow("image", img_test)
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.createTrackbar('BW_blk_size', 'image', 0, int(IMG_SIZE / 2 - 1), lambda x: None)
cv2.createTrackbar('map_blk_size', 'image', 15, NUM_BLKSIZE_CHOICE - 1, lambda x: None)



cv2.waitKey(0)
img_regulate = img_tools.regulateImg(img_test, srcPoints, targetPoints)
cv2.imshow("image_regulate", img_regulate)

img_BW = setFilter()
generateMap(img_BW)
mapGenerated = True
#标定终点
cv2.setMouseCallback("img_virtual", on_EVENT_LBUTTONDOWN)
cv2.waitKey(0)
#