import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt

from IPM_config import *
'''
注意事项：
- 在标定时尽可能占满画面，这样可以最大程度保证IPM还原的区域和效果
'''

def get_calibration_params(img, StandSquare_location):
    '''
    将记录的标定物体的坐标位置输入，进行逆透视变换
    '''
    # 标定
    # jpg中正方形标定物的四个角点(左上、右上、左下、右下),与变换后矩阵位置
    standard_loc = np.float32(StandSquare_location)
    for corner in standard_loc:
        cv2.circle(img, (int(corner[0]), int(corner[1])), 5, (0,0,255), -1) # 画出标定点坐标
    
    l_bot = standard_loc[0]
    r_bot = standard_loc[1]
    l_top = standard_loc[2]
    r_top = standard_loc[3]
    # 以最长边作为基线，即StandSquare的pixel尺寸
    standard_edge = (r_top[0] - l_top[0]) # 标定物最长边
    center_x = l_top[0] + (r_top[0] - l_top[0])/2
    center_y = l_top[1] + (r_top[1] - l_bot[1])/2
    
    left = center_x - standard_edge*StandSquare_num[0]/2 + Extra_pixel
    right = center_x + standard_edge*StandSquare_num[0]/2 + Extra_pixel
    bot = center_y - standard_edge*StandSquare_num[1]/2 + Extra_pixel
    top = center_y + standard_edge*StandSquare_num[1]/2 + Extra_pixel
    img_loc = np.float32([[left, bot],[right, bot],[left,top],[right,top]])

    # 生成透视变换矩阵
    transform_matrix = cv2.getPerspectiveTransform(standard_loc, img_loc)
    
    return img, transform_matrix
    
def calibration(args):
    '''
    calibrate the img by transform matrix
    '''
    img = cv2.imread(args.image)
    img, transform_matrix = get_calibration_params(img, StandSquare_location)
    # 逆透视变换
    calibrated_img = cv2.warpPerspective(img, transform_matrix, BevMap_size, borderMode=cv2.BORDER_TRANSPARENT)
    print(transform_matrix)
    write_matrix(transform_matrix)
    
    plt.subplot(1,2,1)
    plt.title('original img')
    plt.imshow(img[:, :, ::-1]) # 将BGR转化为RGB
    plt.subplot(1,2,2)
    plt.title('IPM img')
    calibrated_img = cv2.resize(calibrated_img, (img.shape[1], img.shape[0]))
    plt.imshow(calibrated_img[:, :, ::-1])
    plt.show()

def write_matrix(matrix, save_dir="./"):
    import os
    np.save(os.path.join(save_dir,"transform_matrix.npy"), matrix)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--image", 
                    default="images\out_blindroad3.jpg",
                    help="image to be celibrated")
    args = parser.parse_args()


    calibration(args)
