import cv2
import numpy as np

import platform
import time

#read the image
small = 0
big = 0
img = cv2.imread('nut.jpg')
cv2.imshow('original', img)
#gray scalling

gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Thresholding

_, threshold = cv2.threshold(gray_scale, 50, 255, cv2.THRESH_BINARY)

#detect the contours

contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:

    (x, y, w, h) = cv2.boundingRect(cnt)
   
    #finding the area of the nut

    area = cv2.contourArea(cnt)
    cv2.putText(img, str(area), (x,y), 0, 1, (255,0,0) )

    #distinguish the small nuts

    if area >1000:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
        big = big+1
    if area < 1000:
         cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
         small = small+1

print("Total number of big nuts: ", big)
print("Total number of small nuts: ", small)
cv2.imshow('contours', img)
cv2.waitKey(0)
cv2.destroyAllWindow()