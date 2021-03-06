#   MIT License
#
#   Copyright (c) 2022 Luke Ingram
#   
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#   
#   main.py

import os,sys 
from scripts.image import Img
import cv2
import threading


#TODO investegate pixel loss in pdf output

def convert(img,imgpath,dest,save): 
    try: 
        if dest[-1] != '/': 
            dest += '/'
        basename = os.path.splitext(os.path.basename(imgpath))[0]
        image = Img(basename,img)
        if save: 
            savepath = "img/dewarp/" + basename
            if not os.path.isdir(savepath):
                os.mkdir(savepath)
            worker = threading.Thread(target=image.saveAll,args=(savepath,))
            worker.start()
            worker.join()
        f = open(dest+basename+'.pdf',"wb+")
        f.write(image.getPdf())
        f.close()
        return 0
    except IOError as e: 
        return -1
    

def main(imgpath,dest,save): 
    (stauts,msg) = (-1,"unknown error")
    if os.path.splitext(imgpath)[1] not in {".jpeg",".png",".jpg",".tiff",".tif",".JPG"}:
        (status,msg) = (-1,"unsupported file format")
    elif not os.path.isdir(dest): 
        (status,msg) = (-1,"destination directory not found")
    elif not os.path.isfile(imgpath): 
        (status,msg) = (-1,"specified image not found")
    else:
        img = cv2.imread(imgpath)
        if img.size == 0: 
            (status,msg) = (1,"unable to open specified file")
        else: 
            if convert(img,imgpath,dest,save) < 0:
                (status,msg) = (1,"unable to create pdf")
            else:
                (status,msg) = (0,"conversion successful")
    return (status,msg)
