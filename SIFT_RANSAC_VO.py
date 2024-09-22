'''
@author: Shaik Althaf (sav4)
- Modfied for Own datset and SIFT Tracking
- Better Outlier rejection 
- Imporved flow tracking - minimized dynamic object keypoint selection 
- Scene -based maskin
- Semantic segmentation maskign (remaining)

@refernce: https://github.com/mtszkw/visual-odometry
'''

import cv2
import plyfile
import numpy as np
import matplotlib.pyplot as plt

from utils import drawFrameFeatures, updateTrajectoryDrawing, savePly
from kitti_reader import DatasetReaderKITTI
from feature_tracking import FeatureTracker



#%%
if __name__ == "__main__":
    tracker = FeatureTracker()
    #detector = cv2.GFTTDetector_create()
    detector = cv2.xfeatures2d.SIFT_create()
    path = 'G:/My Drive/CS445_Project/KITTI_data/data_odometry_gray/dataset/sequences/00/'
    dataset_reader = DatasetReaderKITTI(path)
    #dataset_reader = DatasetReaderKITTI("../videos/KITTI/sequences/00/")

    #K = dataset_reader.readCameraMatrix()
    # K Mobile phone calibrated  : 1920x1080
    K = np.array([[1.632972333291542e+03,    0,     960],
                 [  0,     1.632972333291542e+03,  540],
                 [  0,       0,       1    ]]) 
#%
    prev_points = np.empty(0)
    prev_frame_BGR = dataset_reader.readFrame(0)
    kitti_positions, track_positions = [], []
    camera_rot, camera_pos = np.eye(3), np.zeros((3,1))
    T_prev = np.zeros((3,1))
    plt.show()

    # Process next frames
    for frame_no in range(1,250):
        curr_frame_BGR = dataset_reader.readFrame(frame_no)
        prev_frame = cv2.cvtColor(prev_frame_BGR, cv2.COLOR_BGR2GRAY)
        curr_frame = cv2.cvtColor(curr_frame_BGR, cv2.COLOR_BGR2GRAY)

        # Feature detection & filtering
        prev_points = detector.detect(prev_frame)
        prev_points = cv2.KeyPoint_convert(sorted(prev_points, key = lambda p: p.response, reverse=True))
        print(frame_no)
        
        # Mask based Keypopint selection
        prev_out_idx  = np.where ((prev_points[:,1] < 650))
        prev_points = np.delete(prev_points, prev_out_idx, axis=0)
        
        prev_out_idx  = np.where ((prev_points[:,1] > 800))
        prev_points = np.delete(prev_points, prev_out_idx, axis=0)
        
        r = 600
        dr = 700     
        prev_out_idx  = np.where(abs(prev_points[:,0] - r - dr/2.) >= dr/2.)
        prev_points = np.delete(prev_points, prev_out_idx, axis=0)
        
        #prev_points = prev_points[0:100,:]
        # Feature tracking (optical flow)
        prev_points, curr_points = tracker.trackFeatures(prev_frame, curr_frame, prev_points, removeOutliers=True)
        print (f"{len(curr_points)} features left after feature tracking.")
    
        
        # Essential matrix, pose estimation
        E, mask = cv2.findEssentialMat(curr_points, prev_points, K, cv2.RANSAC, 0.99, 0.9, None)
        prev_points = np.array([pt for (idx, pt) in enumerate(prev_points) if mask[idx] == 1])
        curr_points = np.array([pt for (idx, pt) in enumerate(curr_points) if mask[idx] == 1])
     
        
        _, R, T, _ = cv2.recoverPose(E, curr_points, prev_points, K)
        print(f"{len(curr_points)} features left after pose estimation.")
        actual_scale = np.sqrt((T[0,0]-T_prev[0,0])**2 + (T[1,0]-T_prev[1,0])**2  + (T[2,0]-T_prev[2,0])**2)
        T_prev = T
        # Read groundtruth translation T and absolute scale for computing trajectory
        kitti_pos, kitti_scale = dataset_reader.readGroundtuthPosition(frame_no)
        
        print("act scale",actual_scale)
        kitti_scale =1
        if actual_scale <= 0.001:
            continue

        camera_pos = camera_pos + actual_scale * camera_rot.dot(T)
        camera_rot = R.dot(camera_rot)
        #print("cam pos",camera_pos)

        kitti_positions.append(kitti_pos)
        track_positions.append(camera_pos)
        #updateTrajectoryDrawing(np.array(track_positions), np.array(kitti_positions))
        updateTrajectoryDrawing(np.array(track_positions), np.array(kitti_positions))
        drawFrameFeatures(curr_frame, prev_points, curr_points, frame_no)

        if cv2.waitKey(1) == ord('q'):
            break
            
        prev_points, prev_frame_BGR = curr_points, curr_frame_BGR
        
    cv2.destroyAllWindows()

#%% Save path

gt_pos_arr = np.array(kitti_positions)
track_pos_arr = np.array(track_positions).reshape((len(track_positions),3))

np.save('bloom_turn_SIFT.npy',track_pos_arr)
# new_num_arr = np.load('bloom_turn_SIFT.npy') # load


#%% Compute RMS error

gt_pos_arr = np.array(kitti_positions)
track_pos_arr = np.array(track_positions).reshape((len(track_positions),3))

rmspe = np.sqrt(np.mean(np.square(((gt_pos_arr - track_pos_arr) / gt_pos_arr)), axis=0))
print(rmspe)

RMS_total = np.mean(rmspe[0:2])
print(RMS_total)

