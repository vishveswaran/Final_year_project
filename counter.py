import requests
import platform
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DEVICE_LABEL = "people"  # Replace by your desired device label
VARIABLE_LABEL = "counter"  # Replace by your desired counter variable label
UBIDOTS_TOKEN = "BBFF-pUCt0O6mhWNZd1qomM29zbkCJbJNX5"  # Add here your Ubidots token


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
    count = 0
    people_count = 0
    while True:
        # Verifies if the sensor is activated by a movement
        state = GPIO.input(23)
        if state == False:
            count = count+1
            
        req = send_data_to_ubidots(UBIDOTS_TOKEN, DEVICE_LABEL,
                                       VARIABLE_LABEL, count)
        
        print(count)

if __name__ == "__main__":
    python_version = platform.python_version_tuple()
    if int(python_version[0]) < 3 or int(python_version[0]) >= 3 and int(python_version[1]) < 5:
        print("please upgrade your python version to python 3.6, cancelling routine")
    else:
        main()
