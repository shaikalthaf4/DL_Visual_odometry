# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 21:59:36 2020

@author: shaik
"""

import os
import cv2

import numpy as np
from math import floor
from numpy.linalg import svd, inv
import ffmpeg

from matplotlib import pyplot as plt


def vidwrite_from_numpy(fn, images, framerate=30, vcodec='libx264'):
    ''' 
      Writes a file from a numpy array of size nimages x height x width x RGB
      # source: https://github.com/kkroening/ffmpeg-python/issues/246
    '''
    if not isinstance(images, np.ndarray):
        images = np.asarray(images)
    n,height,width,channels = images.shape
    process = (
        ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
            .output(fn, pix_fmt='yuv420p', vcodec=vcodec, r=framerate)
            .overwrite_output()
            .run_async(pipe_stdin=True)
    )
    for frame in images:
        process.stdin.write(
            frame
                .astype(np.uint8)
                .tobytes()
        )
    process.stdin.close()
    process.wait()

def imageFolder2mpeg(input_path, output_path='./output_video.mpeg', fps=30.0):
    '''
    Extracts the frames from an input video file
    and saves them as separate frames in an output directory.
    Input:
        input_path: Input video file.
        output_path: Output directorys.
        fps: frames per second (default: 30).
    Output:
        None
    '''

    dir_frames = input_path
    files_info = os.scandir(dir_frames)

    file_names = [f.path for f in files_info if f.name.endswith(".jpg")]
    file_names.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    frame_Height, frame_Width = cv2.imread(file_names[0]).shape[:2]
    resolution = (frame_Width, frame_Height)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MPG1')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)

    frame_count = len(file_names)

    frame_idx = 0

    while frame_idx < frame_count:


        frame_i = cv2.imread(file_names[frame_idx])
        video_writer.write(frame_i)
        frame_idx += 1

    video_writer.release()
    


def video2imageFolder(input_file, output_path):
    '''
    Extracts the frames from an input video file
    and saves them as separate frames in an output directory.
    Input:
        input_file: Input video file.
        output_path: Output directorys.
    Output:
        None
    '''

    cap = cv2.VideoCapture()
    cap.open(input_file)

    if not cap.isOpened():
        print("Failed to open input video")

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    frame_idx = 0

    while frame_idx < frame_count:
        ret, frame = cap.read()

        if not ret:
            print ("Failed to get the frame {}".format(frameId))
            continue

        out_name = os.path.join(output_path, 'f{:04d}.jpg'.format(frame_idx+1))
        ret = cv2.imwrite(out_name, frame)
        if not ret:
            print ("Failed to write the frame {}".format(frame_idx))
            continue

        frame_idx += 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)


def video2imageFolder_gray(input_file, output_path):
    '''
    Extracts the frames from an input video file
    and saves them as separate frames in an output directory.
    Input:
        input_file: Input video file.
        output_path: Output directorys.
    Output:
        None
    '''

    cap = cv2.VideoCapture()
    cap.open(input_file)

    if not cap.isOpened():
        print("Failed to open input video")

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    frame_idx = 0
    
    while frame_idx < frame_count:
    #while frame_idx < 200:
        ret, frame = cap.read()

        if not ret:
            print ("Failed to get the frame {}".format(frameId))
            continue

        out_name = os.path.join(output_path, '{:06d}.png'.format(frame_idx))
        ret = cv2.imwrite(out_name, frame[:,:,0])
        if not ret:
            print ("Failed to write the frame {}".format(frame_idx))
            continue

        frame_idx += 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
#%%
    
in_path  = "G:/My Drive/CS445_Project/Althaf/Video2frames/bloom_city.mp4"
out_path  = "G:/My Drive/CS445_Project/Althaf/Video2frames/mob_output/"

out_path_car = "G:/My Drive/CS445_Project/KITTI_data/data_odometry_gray/dataset/sequences/00/ownV1/"


out_path_bloom_turn = "G:/My Drive/CS445_Project/KITTI_data/data_odometry_gray/dataset/sequences/00/bloom_turn/"

out_path_bloom_turn1 = "G:/My Drive/CS445_Project/KITTI_data/data_odometry_gray/dataset/sequences/00/qasim_champaign_back/"


out_path_qasim_kfc = "G:/My Drive/CS445_Project/KITTI_data/data_odometry_gray/dataset/sequences/00/qasim_champaign_kfc_low/"


out_path_bloom_city = "G:/My Drive/CS445_Project/KITTI_data/data_odometry_gray/dataset/sequences/00/bloom_city/"


#%%

video2imageFolder_gray(in_path, out_path_bloom_city) 


#%%
input_file = in_path
cap = cv2.VideoCapture()
cap.open(input_file)

if not cap.isOpened():
    print("Failed to open input video")

frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

frame_idx = 0    

#%%

ret, frame = cap.read()
out_name = os.path.join(out_path,'f{:04d}.jpg'.format(frame_idx+1))
out_name = os.path.join(out_path,'f{:04d}.jpg'.format(frame_idx+1))
ret1 = cv2.imwrite(out_name, frame)
        
#%%
fig, ax = plt.subplots()
#ax.imshow(curr_frame[:,:,[2,1,0]])
ax.imshow(frame)



#%%

