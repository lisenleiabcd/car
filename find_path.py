#!/usr/bin/python3
# -*- coding: utf-8 -*-

#####################################################
#
# bfs寻路模块
#
####################################################
import queue
import numpy as np

bias = ((-1, 0), (0, -1), (0, 1), (1, 0))

def bfs(map, mapSize, desIJ, startIJ):
    routine = np.empty((mapSize, mapSize), dtype=tuple)
    que = queue.Queue()
    que.put_nowait(startIJ)
    routine[startIJ[0]][startIJ[1]] = (-1, -1)

    while (not que.empty()):
        tmp = que.get_nowait()
        if (tmp[0] == desIJ[0] and tmp[1] == desIJ[1]):
            break
        else:
            for i in range(4):
                newX = tmp[0] + bias[i][0]
                newY = tmp[1] + bias[i][1]
                if (newX < mapSize and newX >= 0 and newY < mapSize and newY >= 0 \
                    and routine[newX][newY] is None and map[newX][newY] == 255):
                    que.put_nowait((newX, newY))
                    routine[newX][newY] = tmp

    tmp = desIJ
    routine_ret = np.empty((mapSize, mapSize), dtype=tuple)
    while (tmp != startIJ):
        father = routine[tmp[0]][tmp[1]]
        routine_ret[father[0]][father[1]] = tmp
        tmp = father

    return routine_ret
