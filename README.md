# **Visual Odometry using Classical and Deep Learning Approaches**

This repository contains implementations of Visual Odometry (VO) using both classical feature-based methods (SIFT + RANSAC) and deep learning methods (SuperPoint + RANSAC). The aim is to provide a comparative analysis of the two methods in vehicle path tracking scenarios.

## **Motivation**
Camera pose estimation plays a crucial role in Augmented Reality (AR), Simultaneous Localization and Mapping (SLAM), and autonomous navigation. Accurate pose estimation is particularly challenging due to the dynamic nature of real-world scenes. This project seeks to improve the classical geometric-based approach and compare it with modern deep learning techniques for VO, offering insights into their performance in real-world applications like autonomous driving.

## **Implemented Pipelines**

### **1. SIFT + RANSAC Pipeline (Classical Approach)**
- **Keypoint Detection**: Detects keypoints using SIFT and tracks them across frames using OpenCV's sparse optical flow.
- **Outlier Rejection**: Implements RANSAC to reject outliers and estimate an essential matrix for pose recovery.
- **Scene-based Masking**: Applies scene knowledge-based masking to reduce noise from irrelevant keypoints (e.g., sky, frame edges).
- **Evaluation**: Quantitatively evaluated on the [KITTI Visual Odometry Dataset](http://www.cvlibs.net/datasets/kitti/eval_odometry.php).

### **2. SuperPoint + RANSAC Pipeline (Deep Learning Approach)**
- **Keypoint Detection**: Utilizes SuperPoint, a fully convolutional neural network trained on the MS-COCO dataset, to detect keypoints.
- **Outlier Rejection**: Integrates with RANSAC to filter outlier points, followed by essential matrix computation.
- **Flow Tracking**: Minimizes dynamic object keypoints, focusing on static elements in the scene.
- **Evaluation**: The learning-based framework is also tested on the KITTI dataset, providing a comparative analysis with the classical method.

## **Key Features**
- **Dataset Compatibility**: Primarily uses the KITTI dataset. We have also collected our own dataset using a smartphone-mounted camera, allowing for evaluation on diverse scenarios.
- **Scene-based Masking**: A novel scene-based masking technique to filter irrelevant regions (e.g., sky, dynamic objects), significantly improving pose estimation accuracy.
- **Pretrained Models**: Includes pretrained SuperPoint weights for easy replication of results.
  
## **Results**
Our experiments indicate that:
- The classical SIFT + RANSAC pipeline achieves better performance when optimized with scene-based masking (RMS error reduced from 14.3 to 2.44 on KITTI Seq-03).
- The SuperPoint + RANSAC pipeline offers comparable results to the classical approach but may require more carefully crafted masks for dynamic environments.

Detailed results and visualizations, including comparisons with ground truth trajectories, are available in the [project report](Report.pdf) and our [video explanation](https://www.youtube.com/watch?v=o0zFLPSKSic).


## ** Data Structure**
For detailed instructions on how to organize the dataset, refer to the following structure:

-- KITTI_data (data_odometry_gray, data_odometry_poses, data_odometry_calib)
    |-- data_odometry_gray
    |-- data_odometry_pose
    |-- data_odometry_calib

## **Challenges & Innovations**
- Dynamic Object Filtering: Developing an automated semantic segmentation approach to exclude dynamic objects (e.g., vehicles) for more reliable pose estimation.
- Scene-based Masking: Demonstrated significant error reduction through scene-based filtering of keypoints, particularly in scenarios involving static camera poses or irrelevant features.

## **References**
SuperPoint: Self-Supervised Interest Point Detection and Description [DeTone et al., 2018](https://arxiv.org/abs/1712.07629)

## **Future Work**
We aim to incorporate automated masking techniques using semantic segmentation for enhanced keypoint selection in dynamic environments, making this framework more robust for real-world autonomous navigation systems




####################

# Visual Odometry


## SIFT_plus_RANSAC
@ Details of Implementation:
- Modfied for Own dataset and SIFT Tracking
- Better Outlier rejection 
- Imporved flow tracking - minimized dynamic object keypoint selection 
- Scene -based masking

### Setup and excecution :
1. **DatasetReaderKITTI** is responsible for loading frames from [KITTI Visual Odometry Dataset](http://www.cvlibs.net/datasets/kitti/eval_odometry.php)
2. Run keypoint detection using SIFT and then track these keypoints with **FeatureTracker** that uses OpenCV Sparse optical flow
3. Load calib.txt and poses.txt for the corresponding sequecne from [KITTI Visual Odometry Dataset], and Update Trajectory path while execution.
4. Scene-based masking: Mask sky region (1/4th of top frame) and edges of frame
5. Tune RANSAC theshold (if required) 

# own-dataset
1. Convert video to frames (resize if needed)
2. Setup data_directory to folder with video_frames

## SuperPoint_plus_RANSAC
@ Details of Implementation:
- Modfied for Own dataset and Superpoint Tracking
- Coupled with RANSAC for Outlier rejection 
- flow tracking - minimized dynamic object keypoint selection 

### Setup and excecution 
ipython notebook:
This is the MagicLeap's implementation of SuperPoint
1. Load the pretrained weights for SuperPoint on MS-COCO [here](https://github.com/magicleap/SuperPointPretrainedNetwork/blob/master/superpoint_v1.pth)
2. Run the modified code to obtain optical flow track points generated by the tracker function 
3. Tune RANSAC theshold (if required) 
Creates comprartive plots for ground truth and proposed trajectories.

## KITTI dataset
### Raw data structure
- Download odometry data (grey) synced + rectified from [here](http://www.cvlibs.net/datasets/kitti/eval_odometry.php).
- Copy the ground truth poses from [here] (http://www.cvlibs.net/download.php?file=data_odometry_poses.zip)

```
`-- KITTI_data (data_odometery_gray, data_odometery_poses, data_odometery_calib)
|   |-- data_odometry_gray
|   |   |-- 00
|   |   |   |-- image_00/
|   |   |   `-- ...
|   |   |-- ...
|   |   `-- 01
|   |   |   |-- image_00/
|   |   |   `-- ...
|   |   |-- ...
|   |-- data_odometery_pose
|   |   |-- dataset
|   |   |   |-- poses
|   |   |   |   |--00.txt
|   |   |-- |-- |...
|   |-- data_odometery_calib
|   |   |-- dataset
|   |   |   |-- sequences
|   |   |   |   |--00/
|   |   |   |   |  |--calib.txt
|   |   |   |   `-- ...


