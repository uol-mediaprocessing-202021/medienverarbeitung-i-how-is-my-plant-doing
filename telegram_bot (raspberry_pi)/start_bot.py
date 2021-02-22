#!/usr/bin/python3.7

import bot_api as bot
import requests
import json
import cv2
from time import sleep
import tensor

bot_token = '1591571709:AAGvkGUz3f-VR1CLqs304RxhjrFOFRFGCwY'
url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
polling_rate = 3
# Globals
image_path = '/home/pi/mediaprocessing/images/plant.jpg'
image_masked_path = '/home/pi/mediaprocessing/images/plant_masked.jpg'
image_canny_path = '/home/pi/mediaprocessing/images/plant_cannied.jpg'
HSV_LIGHT_GREEN = (30,100, 80)
HSV_DARK_GREEN = (105,255,255)
IP_CAM_URL = 'http://192.168.50.194/live'

# Maskingfunction
def create_green_mask(img):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, HSV_LIGHT_GREEN, HSV_DARK_GREEN)
    return cv2.bitwise_and(img, img, mask=mask)

def capture_image():
  ip_video = cv2.VideoCapture(IP_CAM_URL)
  ret, frame = ip_video.read()
  cv2.imwrite(image_path, frame)
  ip_video.release()

while True:
    sleep(polling_rate)
    response = requests.get(url)
    parsed = response.json()
    text = parsed['result'][0]['message']['text']
    if text:
        if text == 'How is my plant doing?':
            capture_image()
            img = cv2.imread(image_path)
            masked = create_green_mask(img)
            cv2.imwrite(image_masked_path, masked)
            #canny = cv2.Canny(masked,100,200)
            #cv2.imwrite(image_canny_path, canny)
            label = tensor.get_label_of_image(image_masked_path)
            if label[1] == 'fresh':
                bot.send_text(f'I would say your _{label[0]}_ looks *good*!')
            else:
                bot.send_text(f'I would say your _{label[0]}_ looks *dry*! You better water it 💧')
            bot.send_image(image_masked_path)
        else:
            bot.send_text('I dont understand what you want!')