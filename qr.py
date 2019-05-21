import qrcode, pyqrcode
import time
import pylab as pl
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import image
import png
#import cv2 as cv
from PIL import Image

def createqr(chunks):
    j = 1
    pics = []
    fig = plt.figure()
    long = len(chunks)
    for chunk in chunks:
        #print("Test" + str(j))
        qr = qrcode.QRCode(version=8, error_correction=qrcode.constants.ERROR_CORRECT_L)
        largo = str(j) + "/" + str(long)
        #largo = largo.encode()
        #print("%s%s" % (largo, chunk))
        #qr.add_data("%s%s" % (largo, chunk))
             
        #img = qr.make_image()
        chunk = largo.encode() + b' ||| ' + chunk
        qr.add_data(chunk)
        qr.make(fit=True) 
        print(chunk)
        # img = pyqrcode.create(chunk, error='L', version=8, mode='binary', encoding='cp1252')
        # img.png('code.png', scale=6)
        #img = cv.imread('code.png')
        # img = Image.open('code.png')
        img = qr.make_image(fill_color="black", back_color="white")
        #img.show()
        pic = plt.imshow(img, animated=True)   
        pics.append([pic])
        j = j+1

    ani = animation.ArtistAnimation(fig, pics, interval=270, blit=True, repeat_delay=500)
    plt.show()
    
CHUNK_SIZE = 128
def chunkit(file):
    chunks=[]
    with open(file, 'rb') as infile:
        chunks.append(file.encode())
        while True:
            chunk = infile.read(CHUNK_SIZE)
            if not chunk: break
            chunks.append(chunk)
    return chunks


def main():
    chunks = chunkit("fondo.jpg")
    createqr(chunks)
    
  
if __name__ == "__main__":
    main()