import time
import requests
import math
import random
import cv2
import numpy as np

TOKEN = "BBFF-pUCt0O6mhWNZd1qomM29zbkCJbJNX5"  # Put your TOKEN here
DEVICE_LABEL = "machine"  # Put your device label here 
VARIABLE_LABEL_1 = "small"  # Put your first variable label here
VARIABLE_LABEL_2 = "big"  # Put your second variable label here
VARIABLE_LABEL_3 = "total"  # Put your second variable label here


def build_payload(variable_1, variable_2, variable_3):
    # Creates two random values for sending data
    
    value_1, value_2 = camera()
    value_3 = value_1+value_2
    # Creates a random gps coordinates
    lat = random.randrange(34, 36, 1) + \
        random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(-83, -87, -1) + \
        random.randrange(1, 1000, 1) / 1000.0
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: value_3}

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")

def camera():
    
    small = 0
    big = 0
    img = cv2.imread('nut1.jpg')
    cv2.imshow('original', img)
    #gray scalling

    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Thresholding

    _, threshold = cv2.threshold(gray_scale, 50, 255, cv2.THRESH_BINARY)

    #detect the contours

    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
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
    key = cv2.waitKey(1)
    if key == 27:
        
        cv2.destroyAllWindow()
    return big, small

if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)