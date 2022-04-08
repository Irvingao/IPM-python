import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from IPM_config import *

def IPM_transform(args):
    if args.video != None:
        IPM_video(args)
    else:
        img = cv2.imread(args.image)
        transform_matrix = np.load(args.matrix)
        
        calibrated_img = cv2.warpPerspective(img, transform_matrix, BevMap_size, borderMode=cv2.BORDER_TRANSPARENT)

        plt.subplot(1,2,1)
        plt.title('original img')
        plt.imshow(img[:, :, ::-1]) # 将BGR转化为RGB
        plt.subplot(1,2,2)
        plt.title('IPM img')
        calibrated_img = cv2.resize(calibrated_img, (img.shape[1], img.shape[0]))
        plt.imshow(calibrated_img[:, :, ::-1])
        plt.show()

def IPM_video(args):
    video = cv2.VideoCapture(args.video)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    output_size = (int(BevMap_size[0]*args.resize_scale), int(BevMap_size[1]*args.resize_scale))
    if not os.path.exists(args.save_dir):
        os.mkdir(args.save_dir)
    out = cv2.VideoWriter(os.path.join(args.save_dir, 'output.avi'),fourcc, 30.0, output_size)
    
    transform_matrix = np.load(args.matrix)
    n = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        calibrated_img = cv2.warpPerspective(frame, transform_matrix, BevMap_size, borderMode=cv2.BORDER_TRANSPARENT)
        print("processed: {} images.".format(n))
        calibrated_img = cv2.resize(calibrated_img, output_size)
        out.write(calibrated_img)
        n += 1
    video.release()
    out.release()
    print("IPM convert finished!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--image", 
                        default="images\out_blindroad1.jpg",
                        help="the image path")
    parser.add_argument("-v", "--video", 
                        default= None,
                        help="the video path")
    parser.add_argument("-s", "--save-dir", 
                        default="output",
                        help="output video save path")
    parser.add_argument("-o", "--resize-scale", 
                        default=0.2,
                        help="output video resized down scale")
    parser.add_argument("-m", "--matrix", 
                        type=str,
                        default="transform_matrix.npy",
                        help="IPM transform matrix")            
    args = parser.parse_args()

    IPM_transform(args)