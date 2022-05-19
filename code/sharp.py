import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 绘制直方图函数
def grayHist(img):
    h, w = img.shape[:2]
    pixelSequence = img.reshape([h * w, ])
    numberBins = 256
    histogram, bins, patch = plt.hist(pixelSequence, numberBins,facecolor='black', histtype='bar')
    plt.xlabel("gray label")
    plt.ylabel("number of pixels")
    plt.axis([0, 255, 0, np.max(histogram)])
    plt.show()

def sharp_img():
    img = cv.imread("cut.png")
    out = 2.0* img
    # 进行数据截断，大于255的值截断为255
    out[out > 255] = 255
    # 数据类型转换
    out = np.around(out)
    out = out.astype(np.uint8)
    #cv.imshow("img", img)
    #cv.imshow("out", out)
    #print("done")
    cv.imwrite("./result.png",out)

def sharp_ball():
    img = cv.imread("cut.png")
    out = 3.0* img
    # 进行数据截断，大于255的值截断为255
    out[out > 255] = 255
    # 数据类型转换
    out = np.around(out)
    out = out.astype(np.uint8)
    #cv.imshow("img", img)
    #cv.imshow("out", out)
    #print("done")
    cv.imwrite("./result.png",out)