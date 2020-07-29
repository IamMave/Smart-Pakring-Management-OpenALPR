#!/usr/bin/python
import requests
import base64
import json
import cv2
#from threading import *
# Sample image file is available at http://plates.openalpr.com/ea7the.jpg

def alpr():
    IMAGE_PATH = 'image.jpg'
    SECRET_KEY = 'sk_84ab70b5d8b123bb51c0e466'
    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=in&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)

#print(json.dumps(r.json(), indent=2))
    try:
        print({
                'plate':r.json()['results'][0]['plate'], 
                'brand':r.json()['results'][0]['vehicle']['make'][0]['name'],
            'color':r.json()['results'][0]['vehicle']['color'][0]['name'],

        })
    except:
        print('plate cannot be identified')
    image = cv2.imread(IMAGE_PATH)
    cv2.imshow("recieved",image)
    cv2.waitKey(0)==27
    cv2.destroyWindow("recieved")