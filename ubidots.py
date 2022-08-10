import cv2
import numpy as np
import platform
import time
import requests

#ubidots credentials

DEVICE_LABEL = "computer"  # Replace by your desired device label
VARIABLE_LABEL = "small"  # Replace by your desired counter variable label
UBIDOTS_TOKEN = "BBFF-pUCt0O6mhWNZd1qomM29zbkCJbJNX5"  # Add here your Ubidots token

#send data to ubidots

def send_data_to_ubidots(ubidots_token, device_label, variable_label, value):
    try:
        kwargs = {
            "headers": {"X-Auth-Token": ubidots_token, "Content-type": "application/json"},
            "json": {variable_label: value},
            "url": f"https://industrial.api.ubidots.com/api/v1.6/devices/{device_label}",
            "method": "post"
        }

        return requests.request(**kwargs)

    except Exception as e:
        print(
            f"there was an error after attempting to send values, details:\n{e}")
        return None

def main():
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
    cv2.waitKey(0)
    cv2.destroyAllWindow()
    req = send_data_to_ubidots(UBIDOTS_TOKEN, DEVICE_LABEL, VARIABLE_LABEL, small)

if __name__ == "__main__":
    python_version = platform.python_version_tuple()
    if int(python_version[0]) < 3 or int(python_version[0]) >= 3 and int(python_version[1]) < 5:
        print("please upgrade your python version to python 3.6, cancelling routine")
    else:
        main()
