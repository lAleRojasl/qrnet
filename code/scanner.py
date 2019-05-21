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

class DispositivoLector():
    def __init__(self):
        # get the webcam:  
        self.cap = cv2.Videoself.capture(0)

        self.cap.set(3,640)
        self.cap.set(4,480)
        time.sleep(2)

        self.flag = 0
        self.lista = []

        while(self.cap.isOpened()):
            # self.capture frame-by-frame
            ret, frame = self.cap.read()
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
                if(isinstance(decodedObject.data, bytes)):
                    datos = decodedObject.data
                    print(datos)
                    datos = datos.split(b' ||| ')
                    if(len(datos)!=2):
                        print("Error")
                        print(datos)
                    #print(datos)
                    if(self.flag == 0):
                        self.flag = set_size(datos[0])
                    if datos[1] not in self.lista:
                        add_to_list(datos)
                    elif "" not in self.lista:
                        #build_file()
                        print(str(lista))
                        break

            # Display the resulting frame
            cv2.imshow('frame',frame)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('s'): # wait for 's' key to save 
                cv2.imwrite('self.capture.png', frame)     

        # When everything done, release the self.capture
        self.cap.release()
        cv2.destroyAllWindows()
    def set_size(data):
        data = data.decode("utf-8")
        nums = data.split("/")
        return fill_list(int(nums[1]))

    def fill_list(largo):
        for i in range(largo):
            self.lista.append("")
        return -1

    def add_to_list(data):
        num = getnumber(data[0])
        print("Pos: " + str(num))
        self.lista[num-1] = data[1]

    def getnumber(data):
        data = data.decode("utf-8")
        nums = data.split("/")
        return int(nums[0])

    def build_file():
        name = self.lista.pop(0).decode("utf-8")
        print(name)
        file = open(name, "wb")
        for data in self.lista:
            file.write(data)
        file.close()
        print("File Ready")

    def decode(im): 
        # Find barcodes and QR codes
        decodedObjects = pyzbar.decode(im)
        return decodedObjects

