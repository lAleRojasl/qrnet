import qrcode
import time
import pylab as pl
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

class DispositivoLuzAdaptador():
    def __init__(self, message):
        self.CHUNK_SIZE = 128

        self.message = message
        if(len(message.encode('UTF-8')) < 128):
            self.createqr([message.encode('UTF-8')])

    def createqr(self,chunks):
        j = 1
        pics = []
        fig = plt.figure()
        long = len(chunks)
        for chunk in chunks:
            qr = qrcode.QRCode(version=8, error_correction=qrcode.constants.ERROR_CORRECT_L)
            largo = str(j) + "/" + str(long)
            chunk = largo.encode() + b' ||| ' + chunk
            qr.add_data(chunk)
            qr.make(fit=True) 
            img = qr.make_image(fill_color="black", back_color="white")
            pic = plt.imshow(img, animated=True)   
            pics.append([pic])
            j = j+1

        ani = animation.ArtistAnimation(fig, pics, interval=270, blit=True, repeat_delay=500)
        plt.show()
        
    def chunk_file(self,file):
        chunks=[]
        with open(file, 'rb') as infile:
            chunks.append(file.encode())
            while True:
                chunk = infile.read(CHUNK_SIZE)
                if not chunk: break
                chunks.append(chunk)
        return chunks







