import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_location(args):
    '''
    记录标定物体的坐标位置
    param {img}
    return {None}
    '''    
    img = cv2.imread(args.image)
    img[:, :, ::-1] # 是将BGR转化为RGB
    plt.plot()
    plt.imshow(img[:, :, ::-1])
    plt.title('img')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--image", 
                    default="images\out_blindroad3.jpg",
                    help="image to be celibrated")
    args = parser.parse_args()
    
    get_location(args)