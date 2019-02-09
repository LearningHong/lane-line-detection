# -*- coding: utf-8 -*-
# ——author—— = “hong”
# Email :1424148078@qq.com
# time  :
# function:

import cv2
import numpy as np
import time


def white_and_yellow(Img):
    HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)
    # H, S, V = cv2.split(HSV)
    LowerYellow = np.array([0, 70, 70])
    UpperYellow = np.array([80, 255, 255])
    mask_Yellow = cv2.inRange(HSV, LowerYellow, UpperYellow)
    LowerWhite = np.array([0, 0, 100])
    UpperWhite = np.array([180, 30, 255])
    mask_White = cv2.inRange(HSV, LowerWhite, UpperWhite)
    # 开运算
    mask = mask_White + mask_Yellow

    return mask


def set_roi(img):
    roi_left = img[270:500,0:480]
    roi_right = img[270:500,480:960]
    return roi_left,roi_right


def find_line_right(img,blur):
    kernel_size = (7, 7)
    kernel = np.ones((3, 3), np.uint8)
    kernel_1 = np.ones((1, 1), np.uint8)
    sigma = 15

    blur = cv2.GaussianBlur(blur, kernel_size, sigma)
    blur = cv2.erode(blur, kernel, iterations=4)
    blur = cv2.dilate(blur, kernel, iterations=5)
    gauss = cv2.GaussianBlur(blur, kernel_size, sigma)
    # cv2.imshow('blur', gauss)
    edges = cv2.Canny(gauss, 0, 50)
    edges = cv2.erode(edges, kernel_1, iterations=5)
    edges= cv2.dilate(edges, kernel_1, iterations=5)
    minLineLength = 10
    maxLineGap = 11
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, minLineLength, maxLineGap)
    line_mask = np.zeros(edges.shape,np.uint8)
    # print(lines)
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            # print(slope)
            if slope < 1 and slope > 0.4:
                cv2.line(line_mask, (x1, y1), (x2, y2), (255, 255, 255), 5)
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 5)
    cv2.imshow('right',line_mask)


def find_line_left(img,blur):
    kernel_size = (7, 7)
    kernel = np.ones((3, 3), np.uint8)
    kernel_1 = np.ones((1, 1), np.uint8)
    sigma = 15

    blur = cv2.GaussianBlur(blur, kernel_size, sigma)
    blur = cv2.erode(blur, kernel, iterations=4)
    blur = cv2.dilate(blur, kernel, iterations=5)
    gauss = cv2.GaussianBlur(blur, kernel_size, sigma)
    # cv2.imshow('blur', gauss)
    edges = cv2.Canny(gauss, 0, 50)
    edges = cv2.erode(edges, kernel_1, iterations=5)
    edges= cv2.dilate(edges, kernel_1, iterations=5)
    minLineLength = 10
    maxLineGap = 11
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, minLineLength, maxLineGap)
    line_mask = np.zeros(edges.shape, np.uint8)
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            # print(slope)
            if slope < -0.6 and slope > -1:
                cv2.line(line_mask, (x1, y1), (x2, y2), (255, 255, 255), 5)
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 5)
    cv2.imshow('left', line_mask)


def main():
    fpsa = []
    cap = cv2.VideoCapture('D:\python_code\driverless_car\line_tgh/txtxtx/1111.avi')
    while(True):
        # get a frame
        st = time.time()
        ret, frame = cap.read()
        # show a frame
        frame = cv2.resize(frame,(960,580))
        left, right = set_roi(frame)
        mask = white_and_yellow(frame)
        cv2.imshow("mask", mask)
        left_mask, right_mask = set_roi(mask)
        left_img, right_img = set_roi(frame)
        find_line_right(right_img,right_mask)
        find_line_left(left_img, left_mask)
        et = time.time()
        fps = 1/(et-st)
        # print('fps',1/(et-st))
        fpsa.append(fps)
        cv2.imshow("capture", frame)
		#print(np.average(fpsa))
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break
    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()