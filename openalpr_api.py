import requests
import paho.mqtt.client as mqtt
import base64
import json
import sqlite3
from datetime import datetime
import time
import collections
import yaml
import numpy as np
import cv2
import cv2 as open_cv


broker="34.72.249.18"
port=1883

place_name = 'Mantri Mall'


def alpr():

    f= open("config.txt","r")
    arr = {}
    for _ in range(0,2):
        result = f.readline()
        arr[result.split(' : ')[0]] = result.split(' : ')[-1].split('\n')[0]
    f.close()


    url=arr['img_url']
    
    data_file = "data/coordinates_1.yml"
    with open(data_file, "r") as data:
        points = yaml.load(data)
                            
    #take data from file and assign it to flag and slot
    f= open("file.txt","r")
    f1=f.readline()
    f.close()
    
    ind=int(f1[0])
    slot=ind+1
    flag=f1[2]
    
    
    print(slot)
    print(flag)
    now=datetime.now()
    entry_time = now.strftime("%H:%M:%S")
    #flag=int(f1[1])
    

    #CONNECTING TO DATABASE
    conn = sqlite3.connect('minidb.db')
    c = conn.cursor()
    
    #CREATING TABLE
    c.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(plate VARCHAR, brand TEXT, entry_time INT, slot INT PRIMARY KEY)")
    
    if flag=='1':
        list=[]
        d=collections.OrderedDict()
        d['slot_number']=slot 
        d['status']=flag
        d['place_name']=place_name
        list.append(d)
        t=json.dumps(list)
        print(t)

        client1= mqtt.Client("control1")                           #create client objectq
        client1.on_publish = on_publish                          #assign function to callback
        client1.connect(broker,port)                                 #establish connection
        ret= client1.publish("slot_info",t)
       

        time.sleep(5)
        img_resp_pic= requests.get(url)
        img_arr_pic= np.array(bytearray(img_resp_pic.content),dtype=np.uint8)
        frame_crop = cv2.imdecode(img_arr_pic, -1)
        
        temp = points[ind]
        q=temp['coordinates']
        r=[q[0][0],q[1][0],q[2][0],q[3][0]]
        x_max=max(r)
        x_min=min(r)
        r=[q[0][1],q[1][1],q[2][1],q[3][1]]
        y_min=min(r)
        y_max=max(r)
        cropped_image = frame_crop[y_min:y_max,x_min:x_max]
        #open_cv.imshow("Cropped",cropped_image)
        open_cv.imwrite('image.jpg',cropped_image)
        
        #sleep 5 sec
        #crop the image
        IMAGE_PATH = 'image.jpg'
        SECRET_KEY = arr['openalpr_apikey']
        
        
        with open(IMAGE_PATH, 'rb') as image_file:
            img_base64 = base64.b64encode(image_file.read())
        url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=in&secret_key=%s' % (SECRET_KEY)
        r = requests.post(url, data = img_base64)
                
        try:
            '''print({
                    'plate':r.json()['results'][0]['plat']
                    'brand':r.json()['results'][0]['vehicle']['make'][0]['name'],
                    'color':r.json()['results'][0]['vehicle']['color'][0]['name']
                })'''
            #GETTING RESULTS
        
            p=r.json()['results'][0]['plate']
            q=r.json()['results'][0]['vehicle']['make'][0]['name']
            r=r.json()['results'][0]['vehicle']['color'][0]['name']
            
            
        
            print("car came in")
            #INSERTING DATA
            c.execute("INSERT INTO stuffToPlot (plate, brand, entry_time, slot) VALUES (?, ?, ?, ?)",
                  (p,q, entry_time, slot))
            
            conn.commit()
            c.close()
            conn.close() 


        except:
            print('plate cannot be identified')
            
    else:
        now=datetime.now()
        #exit_time=now.strftime("%H:%M:%S")
        
        #RETRIEVING DATA
        c.execute("SELECT * FROM stuffToPlot where slot=?",(slot,)) 
        

       #PRINTING DATA
        rows=c.fetchall()
        objects_list=[]
        for row in rows:
            d=collections.OrderedDict()
            d['number_plate']=row[0]
            d['brand']=row[1] 
            d['entry_time']=row[2]
            d['exit_time']=now.strftime("%H:%M:%S")
            d['slot_number']=row[3]
            d['place_name']=place_name
            objects_list.append(d)
        
        j=json.dumps(objects_list,indent=4)
        
        print(j)
        
        client1= mqtt.Client("control1")                           #create client objectq
        client1.on_publish = on_publish                          #assign function to callback
        client1.connect(broker,port)                                 #establish connection
        ret= client1.publish("getSlotDetails",j)
       
        
        
        
        #DELETING DATA  
        c.execute("DELETE  FROM stuffToPlot WHERE slot=?",(slot,))
        print("database deleted")
    
        
        #CLOSING AND COMMIT CONNECTION
        conn.commit()
        c.close()
        conn.close()
         


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass




    

        
