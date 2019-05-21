# -*- coding: utf-8 -*-
"""
"""
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import re
import struct

# get the webcam:  
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)
#160.0 x 120.0
#176.0 x 144.0
#320.0 x 240.0
#352.0 x 288.0
#640.0 x 480.0
#1024.0 x 768.0
#1280.0 x 1024.0
time.sleep(2)

flag = 0
lista = []

def set_size(data):
    data = data.decode("utf-8")
    nums = data.split("/")
    return fill_list(int(nums[1]))

def fill_list(largo):
    for i in range(largo):
        lista.append("")
    return -1

def add_to_list(data):
    num = getnumber(data[0])
    print("Pos: " + str(num))
    lista[num-1] = data[1]

def getnumber(data):
    data = data.decode("utf-8")
    nums = data.split("/")
    return int(nums[0])


def build_file():
    name = lista.pop(0).decode("utf-8")
    print(name)
    file = open(name, "wb")
    for data in lista:
        file.write(data)
    file.close()
    print("File Ready $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    
def decode(im): 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    #for obj in decodedObjects:
        #print('Type : ', obj.type)
        #print('Data : ', obj.data,'\n')     
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
    decodedObjects = decode(im)

    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
     
        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points;
         
        # Number of points in the convex hull
        n = len(hull)     
        # Draw the convext hull
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)
        #print(x, y)
        #print('Type : ', decodedObject.type)
        #print('Data : ', decodedObject.data,'\n')
        #print(decodedObject.data.decode('utf-8'))
        if(isinstance(decodedObject.data, bytes)):
            datos = decodedObject.data
            print(datos)
            datos = datos.split(b' ||| ')
            if(len(datos)!=2):
                print("Error")
                print(datos)
            #print(datos)
            if(flag == 0):
                flag = set_size(datos[0])
            if datos[1] not in lista:
                add_to_list(datos)
            elif "" not in lista:
                build_file()
                print("LISTO")
                break
        
        #barCode = str(decodedObject.data)
        #cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
               
    # Display the resulting frame
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'): # wait for 's' key to save 
        cv2.imwrite('Capture.png', frame)     

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()