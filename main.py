#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import img_tools
import numpy as np
import car_detect
from find_path import bfs
from matplotlib import pyplot as plt
import math
import time
import chassis
import copy
import sys

thresholdVal = 0
IMG_SIZE = 720

# for coordinate transform
targetPoints = np.float32([[0, 0],
                         [IMG_SIZE, 0],
                         [IMG_SIZE, IMG_SIZE],
                         [0, IMG_SIZE]])
srcPoints = np.float32([[0, 0], [0, 0], [0, 0], [0, 0]])
global nextSrcPtIndex
nextSrcPtIndex = 0

# for generating the map
BLKSIZE = [2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 20, 24, 30, 32, 36, 40, 45, 48, 50, 60, 72, 80, 90, 120]
NUM_BLKSIZE_CHOICE = 25

# for padding the map
bias_map = ((-1, 0), (0, -1), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1))

global mapSize
mapSize = 10
blockSize = 0
bw_arg = 0;
map = []
img_virtual = np.ones((IMG_SIZE, IMG_SIZE), np.uint8)
mapGenerated = False
desIJ = (-1, -1)

# coord transform from real coord to map coord
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
                                                    , i * blockSize : (i + 1) * blockSize]) # 根据一个区域内的均值，判断黑白

                    if (mean > 200):          ########valve value!!!!!!!!!!
                        map[j].append(255)
                        img_virtual[j * blockSize: (j + 1) * blockSize \
                            , i * blockSize: (i + 1) * blockSize] = 255
                    else:
                        map[j].append(0)
                        img_virtual[j * blockSize: (j + 1) * blockSize \
                            , i * blockSize: (i + 1) * blockSize] = 0
            map_save = copy.deepcopy(map)

            for j in range(0, mapSize):                        #对map进行补全，减小小车与边边角角碰撞的概率
                for i in range(0, mapSize):
                    if (map[i][j] == 255):
                        for k in range(8):
                            nexI = i + bias_map[k][0]
                            nexJ = j + bias_map[k][1]
                            if (nexI >= 0 and nexI < mapSize and nexJ >= 0 and nexJ < mapSize \
                                    and map_save[nexI][nexJ] == 0):
                                map[i][j] = 0
                                img_virtual[i * blockSize: (i + 1) * blockSize \
                                    , j * blockSize: (j + 1) * blockSize] = 0
                                break

            map_save.clear()

            cv2.imshow("img_virtual", img_virtual)

        prevChoice = choice
        k = cv2.waitKey(1000) & 0xFF
        if k == 32:
            break

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param): #鼠标点四下确定坐标变换. 同时也用作指定终点
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

client = chassis.chassis()
cv2.namedWindow("image")
cap = cv2.VideoCapture(1)
 #take a frame of the video to define the coord transform

while (1):
    ret, img_test = cap.read()
    cv2.imshow("image", img_test)
    k = cv2.waitKey(1) & 0xFF
    if k == 32:
        break

cv2.imshow("image", img_test)

#设定鼠标点击动作，设定拖动条
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.createTrackbar('BW_blk_size', 'image', 200, int(IMG_SIZE / 2 - 1), lambda x: None)
cv2.createTrackbar('map_blk_size', 'image', 13, NUM_BLKSIZE_CHOICE - 1, lambda x: None)


cv2.waitKey(0)    # 等4个点点点好之后，继续
img_regulate = img_tools.regulateImg(img_test, srcPoints, targetPoints)  #坐标变换
cv2.imshow("image_regulate", img_regulate)

img_BW = setFilter()
cv2.destroyWindow("image_regulate")
generateMap(img_BW)
mapGenerated = True
#choose a point as destination
cv2.setMouseCallback("img_virtual", on_EVENT_LBUTTONDOWN)
cv2.waitKey(0)
###############################################
print("put the car!!!!!!!!!!!!!!")
cv2.waitKey(0)
routine = np.empty((mapSize, mapSize), dtype=tuple)

flag = 0
flag2 = 0
flag3 = 0
img_tmp = copy.copy(img_virtual)

#################################################
#
#  主循环
#
################################################
while (1):
    ret, img = cap.read()
    
    cv2.imshow("image2", img)

    img_regulate = img_tools.regulateImg(img, srcPoints, targetPoints)
    head_coords, tail_coords = car_detect.car_dectect(img_regulate)
    car_center = ((head_coords[0] + tail_coords[0]) / 2, (head_coords[1] + tail_coords[1]) / 2 + 70)

    #cv2.waitKey(0)
    #if function car_dectect return (0, 0), the car is missing 
    if (head_coords[0] == 0 or tail_coords[0] == 0 or head_coords[1] == 0 or tail_coords[1] == 0):
        print("Cannot find the car!")
        #take another photo and then detect again
        ret, img = cap.read()
        cv2.imshow("image_virtual", img_virtual)
        time.sleep(0.05)
        ret, img = cap.read()
        continue

    curIJ = xy2ij(car_center[0], car_center[1])
    #find path to the destination, only execute once
    if (routine[curIJ[0]][curIJ[1]] is None and flag == 0):           
        flag = 1
        routine = bfs(map, mapSize, desIJ, curIJ)
        img_virtual = copy.copy(img_tmp)
        tmp = curIJ
        # draw the routine########################################
        while (1):
            img_virtual[tmp[0] * blockSize: (tmp[0] + 1) * blockSize \
                , tmp[1] * blockSize: (tmp[1] + 1) * blockSize] = 70;
            tmp = routine[tmp[0]][tmp[1]]
            if (tmp == desIJ):
                break;
        cv2.imshow("image_virtual", img_virtual)
        cv2.waitKey(200)
        #######################################
        tmp = routine[curIJ[0]][curIJ[1]]
        tmp2 = (tmp[1] * blockSize, tmp[0] * blockSize)
    #program exit normally
    if (curIJ == desIJ):
        sys.exit()
    #calculate direction of car    
    if (head_coords[1] > tail_coords[1]):
        if (head_coords[0] >= tail_coords[0]):
            theta1 = math.degrees(math.atan(abs(head_coords[0] - tail_coords[0]) / abs(head_coords[1] - tail_coords[1])))
        else:
            theta1 = 360 - math.degrees(math.atan(abs(head_coords[0] - tail_coords[0]) / abs(head_coords[1] - tail_coords[1])))
    elif (head_coords[1] < tail_coords[1]):
        if (head_coords[0] >= tail_coords[0]):
            theta1 = 180 - math.degrees(math.atan(abs(head_coords[0] - tail_coords[0]) / abs(head_coords[1] - tail_coords[1])))
        else:
            theta1 = 180 + math.degrees(math.atan(abs(head_coords[0] - tail_coords[0]) / abs(head_coords[1] - tail_coords[1])))
    else:
        theta1 = 90 * (head_coords[0] - tail_coords[0]) / abs(head_coords[0] - tail_coords[0])

    #update the point where car should go only when car reach current point
    if (routine[curIJ[0]][curIJ[1]] is not None and tmp == curIJ):
        tmp = routine[tmp[0]][tmp[1]]
        tmp2 = (tmp[1] * blockSize, tmp[0] * blockSize)
    #calculate the direction of next point
    if (tmp2[1] > car_center[1]):
        if (tmp2[0] >= car_center[0]):
            theta2 = math.degrees(math.atan(abs(tmp2[0] - car_center[0]) / abs(tmp2[1] - car_center[1])))
        else:
            theta2 = 360 - math.degrees(math.atan(abs(tmp2[0] - car_center[0]) / abs(tmp2[1] - car_center[1])))
    elif (tmp2[1] < car_center[1]):
        if (tmp2[0] >= car_center[0]):
            theta2 = 180 - math.degrees(math.atan(abs(tmp2[0] - car_center[0]) / abs(tmp2[1] - car_center[1])))
        else:
            theta2 = 180 + math.degrees(math.atan(abs(tmp2[0] - car_center[0]) / abs(tmp2[1] - car_center[1])))
    else:
        theta2 = 90 * (tmp2[0] - car_center[0]) / abs(tmp2[0] - car_center[0])
    #angle that car need to turn
    theta = (theta1 - theta2) % 360
    
    if (theta > 90 and theta < 270 and flag3 == 0):
        tmp = routine[tmp[0]][tmp[1]]
        tmp2 = (tmp[1] * blockSize, tmp[0] * blockSize)
        flag3 = 1
    elif (theta <= 90 or theta >= 270):
        flag3 = 0
    
    print("blocksize:", blockSize)
    print("car:", curIJ[0], curIJ[1], car_center[0], car_center[1])
    print("des:", tmp[0], tmp[1], tmp2[0], tmp2[1])
    print("we need:", theta1, theta2, theta)
    #push the command to car
    if (theta <= 180 and theta > 15):
        client.right()
        flag2 = flag2 + 1
        time.sleep(0.1)
    elif (theta < 345 and theta > 180):
        client.left()
        flag2 = flag2 + 1
        time.sleep(0.1)
    else:
        client.forward()
        print("go forward\n")
        flag2 = 0
        time.sleep(0.1)
    client.stop()
    #cv2.waitKey(0)
        
