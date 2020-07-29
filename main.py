import argparse
import cv2
import yaml
import logging
import requests
import numpy as np
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from colors import *


def main():

    print('main executed')
    logging.basicConfig(level=logging.INFO)

    #image_file = "images/park.ing_lot_1.png"
    data_file = "data/coordinates_1.yml"
    start_frame = 400
    video_file = "videos/parking_lot_1.mp4"
    

    f= open("config.txt","r")
    arr = {}
    for _ in range(0,2):
        result = f.readline()
        arr[result.split(' : ')[0]] = result.split(' : ')[-1].split('\n')[0]
    print(arr)
    f.close()
    url=arr['img_url']

    img_resp_pic= requests.get(url)
    img_arr_pic= np.array(bytearray(img_resp_pic.content),dtype=np.uint8)
    img1_pic = cv2.imdecode(img_arr_pic, -1)
    filename='savedImage.jpg'
    cv2.imwrite(filename,img1_pic)
        

    if filename is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(filename, points, COLOR_RED)
            generator.generate()

    with open(data_file, "r") as data:
        points = yaml.load(data)
        detector = MotionDetector(video_file, points, int(start_frame))
        detector.detect_motion()


def parse_args():
    parser = argparse.ArgumentParser(description='Generates Coordinates File')

    parser.add_argument("--image",
                        dest="image_file",
                        required=False,
                        help="Image file to generate coordinates on")

    parser.add_argument("--video",
                        dest="video_file",
                        required=True,
                        help="Video file to detect motion on")

    parser.add_argument("--data",
                        dest="data_file",
                        required=True,
                        help="Data file to be used with OpenCV")

    parser.add_argument("--start-frame",
                        dest="start_frame",
                        required=False,
                        default=1,
                        help="Starting frame on the video")

    return parser.parse_args()


if __name__ == '__main__':
    main()
