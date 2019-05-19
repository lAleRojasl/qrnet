import qrcode
import time
import pylab as pl
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

def createqr(chunks):
    j = 1
    pics = []
    fig = plt.figure()
    long = len(chunks)
    for chunk in chunks:
        #print("Test" + str(j))
        qr = qrcode.QRCode(version=8, error_correction=qrcode.constants.ERROR_CORRECT_L)
        largo = str(j) + "/" + str(long)
        largo = largo.encode()
        print("%s %s" % (largo, chunk))
        qr.add_data("%s %s" % (largo, chunk))
        qr.make(fit=True)      
        img = qr.make_image()
        pic = plt.imshow(img, animated=True)   
        pics.append([pic])
        j = j+1

    ani = animation.ArtistAnimation(fig, pics, interval=50, blit=True, repeat_delay=1000)
    plt.show()
    
CHUNK_SIZE = 128
def chunkit(file):
    chunks=[]
    with open(file, 'rb') as infile:
        chunks.append(file.encode())
        while True:
            chunk = infile.read(CHUNK_SIZE)
            if not chunk: break
            print(chunk)
            chunks.append(chunk)
    return chunks


def main():
    chunks = chunkit("test.txt")
    createqr(chunks)
    
  
if __name__ == "__main__":
    main()