import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import json
from PIL import Image
import glob
import os
import urllib.request

width = 10459
height = 300

d = 512

ids = ["KURE05_01"]

opath = 'test_igaku.sh'

fo = open(opath, "w")

for id in ids:

    odir = "data/"+id + "/tile"

    os.makedirs(odir, exist_ok=True)

    prefix = "https://www.lib.m.u-tokyo.ac.jp/digital/resources/KURE05_01/"+id+"/0"

    w_n = int(width / d) if width % d == 0 else int(width / d) + 1
    h_n = int(height / d) if height % d == 0 else int(height / d) + 1

    for w in range(w_n):

        for h in range(h_n):

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

            filename = str(x1).zfill(5)+str(y1).zfill(5) + \
                str(dx).zfill(5) + str(dy).zfill(5) + ".jpg"

            opath = odir+"/"+filename

            if not os.path.exists(opath):

                urllib.request.urlretrieve(
                    prefix+"/"+filename, opath)

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

            filename = odir+"/"+str(x1).zfill(5)+str(y1).zfill(5) + \
                str(dx).zfill(5) + str(dy).zfill(5) + ".jpg"

            line += filename + " "

    line += "-tile "+str(w_n)+"x"+str(h_n) + \
        " -geometry +0+0 data/"+id+"/"+id+".jpg"
    fo.write(line+"\n")

fo.close()
