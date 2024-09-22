# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 11:17:12 2020

@author: shaik
"""


import cv2
import numpy as np
 
in_path  = "G:/My Drive/CS445_Project/Althaf/Video2frames/car_ownV1.mp4"

cap = cv2.VideoCapture(in_path)
 

#% 1920x 1080
out_size  = (960,540)
fps = 60
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('qasim_champaign_kfc_low.mp4',fourcc, fps, out_size)
 
while True:
    ret, frame = cap.read()
    if ret == True:
        b = cv2.resize(frame,out_size,fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        out.write(b)
    else:
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()



#%%
from matplotlib import pyplot as plt

fig, ax = plt.subplots()
ax.imshow(b[:,:,[2,1,0]])