# **Context-Based Scene Masking to improve Visual Odometry: Classical and Deep Learning Approaches**

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


## **Data Structure**
For detailed instructions on how to organize the dataset, refer to the following structure:

KITTI_data/ 
├── data_odometry_gray/
├── data_odometry_poses/
└── data_odometry_calib/


## **Challenges & Innovations**
- Dynamic Object Filtering: Developing an automated semantic segmentation approach to exclude dynamic objects (e.g., vehicles) for more reliable pose estimation.
- Scene-based Masking: Demonstrated significant error reduction through scene-based filtering of keypoints, particularly in scenarios involving static camera poses or irrelevant features.

## **References**
SuperPoint: Self-Supervised Interest Point Detection and Description [DeTone et al., 2018](https://arxiv.org/abs/1712.07629)

## **Future Work**
We aim to incorporate automated masking techniques using semantic segmentation for enhanced keypoint selection in dynamic environments, making this framework more robust for real-world autonomous navigation systems

