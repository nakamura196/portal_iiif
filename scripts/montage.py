import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import json
from PIL import Image
import glob
import os
import urllib.request

width = 6144
height = 4397

d = 256

ids = ["D-13"]

opath = 'test.sh'

fo = open(opath, "w")

for id in ids:

    odir = "data/"+id

    os.makedirs(odir, exist_ok=True)

    prefix = "http://www.l.u-tokyo.ac.jp/moyoro/resources/"+id+"/0"

    w_n = int(width / d) if width % d == 0 else int(width / d) + 1
    h_n = int(height / d) if height % d == 0 else int(height / d) + 1

    line = "montage "

    for h in range(h_n):

        for w in range(w_n):
        

            x1 = w * d
            y1 = h * d

            x2 = x1 + d
            y2 = y1 + d

            dx = d
            dy = d

            if width < x2:
                dx = width - x1

            if height < y2:
                dy = height - y1

            filename = odir+"/tile/"+str(x1).zfill(5)+str(y1).zfill(5) + \
                str(dx).zfill(5) + str(dy).zfill(5) + ".jpg"

            line += filename + " "

    line += "-tile "+str(w_n)+"x"+str(h_n) + \
        " -geometry +0+0 "+odir+"/"+id+".jpg"
    fo.write(line+"\n")

fo.close()
