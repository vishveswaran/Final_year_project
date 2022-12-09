import time
import requests
import cv2
import numpy as np
from time import sleep
path = "nut.jpg" #Path for the image
cap = cv2.VideoCapture(0)
#Adding ubidots credentials
TOKEN = "BBFF-pUCt0O6mhWNZd1qomM29zbkCJbJNX5"  # Put your TOKEN here
DEVICE_LABEL = "machine"  # Put your device label here 
VARIABLE_LABEL_1 = "WRONG"  # Put your first variable label here
VARIABLE_LABEL_2 = "CORRECT"  # Put your second variable label here
VARIABLE_LABEL_3 = "total"  # Put your second variable label here

big = 0
small = 0
while True:
    

    _,frame = cap.read()
    belt = frame[209: 373, 175: 425]
    img = belt
    
    #img = cv2.imread(path)
    #cv2.imshow('original', img)

    #gray scalling

    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Thresholding

    _, threshold = cv2.threshold(gray_scale, 50, 255, cv2.THRESH_BINARY_INV)

    #detect the contours

    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:

        (x, y, w, h) = cv2.boundingRect(cnt)
    
        #finding the area of the nut

        area = cv2.contourArea(cnt)
        cv2.putText(img, str(area), (x,y), 0, 1, (255,0,0) )
        cv2.imshow("dimension",img)
        #distinguish the small nuts
        
        if area >1000:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
            big = big+1
        if area < 1000:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            small = small+1

    print("Total number of big nuts: ", big)
    print("Total number of small nuts: ", small)
    #cv2.imshow('contours', img)
    key = cv2.waitKey(1)
    if key == 27:
        
        cv2.destroyAllWindow()
    
    total = big+small
    payload = {VARIABLE_LABEL_1: big,
               VARIABLE_LABEL_2: small,
               VARIABLE_LABEL_3: total}
    
    print("Attempting to send the data")
    sleep(0.1)
    
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        #time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        

    print("[INFO] request made properly, your device is updated")
    
    
    


    
    
    
    
    