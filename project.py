# Linfeng Li
# Xing Qian
# CS 415 Final Project
# University of Illinois at Chicago
# 11/13/2020

import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import math


def main():
    plt.gray()
    barcode_path = './barcode.jpg'
    img = cv2.imread(barcode_path, 0)
    plt.imshow(img)
    plt.show()

    return


if __name__ == '__main__':
    main()