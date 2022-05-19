import cv2 as cv
import numpy as np
import math
import sharp
import cut
import serial
import re
import angle
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)
GPIO.setup(35, GPIO.IN)

ser = serial.Serial('/dev/ttyS0', 9600,timeout=10)
coefficient = [0.3097,0.3241,0.3365,0.3517,0.3645,0.3825,0.3954,0.4093,0.4268,0.4457,0.4695,0.4877]

tmp = 0
Distance = 0.0
decade =0
X_angle=0
Y_angle=0

def distance():
    global tmp
    all = 0.0
    global Distance
    global decade
    data = ser.read(100)
    print(data)
    str_num=(re.findall(r"\d+\.?\d",data.decode('utf-8')))
    print(str_num)
    long = len(str_num)
    for num in range(0,long):
        if(float(str_num[num])>100):
            all += float(str_num[num])
            tmp+=1
            print(tmp,all)
    Distance=all/tmp
    print("距离"+"%.2f"%(Distance))
    flag=0
    if (Distance>200):
        flag=Distance-200
    if (Distance<200):
        flag=200-Distance
    decade = int(flag /10)
    tmp = 0
    dis_relay()
    Distance =0.0

class ShapeAnalysis:

    def __init__(self):
        self.shapes = {'triangle': 0, 'rectangle': 0, 'polygons': 0, 'circles': 0}

    def analysis(self, frame):
        h, w, ch = frame.shape
        global coefficient
        global Distance
        result = np.zeros((h, w, ch), dtype=np.uint8)
        print("start to detect lines...\n")
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        
        distance()
        
        contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in range(len(contours)):
            cv.drawContours(result, contours, cnt, (0, 255, 0), 2)

            epsilon = 0.01 * cv.arcLength(contours[cnt], True)
            approx = cv.approxPolyDP(contours[cnt], epsilon, True)

            corners = len(approx)
            shape_type = ""
            if corners == 3:
                count = self.shapes['triangle']
                count = count+1
                self.shapes['triangle'] = count
                shape_type = "三角形"
            if corners == 4:
                count = self.shapes['rectangle']
                count = count + 1
                self.shapes['rectangle'] = count
                shape_type = "矩形"
            if corners >= 10:
                count = self.shapes['circles']
                count = count + 1
                self.shapes['circles'] = count
                shape_type = "圆形"
            if 4 < corners < 10:
                count = self.shapes['polygons']
                count = count + 1
                self.shapes['polygons'] = count
                shape_type = "矩形"


            global X_angle
            global Y_angle

            p = cv.arcLength(contours[cnt], True)
            area = cv.contourArea(contours[cnt])

            if(p>250):
                mm = cv.moments(contours[cnt])
                cx = int(mm['m10'] / mm['m00'])
                cy = int(mm['m01'] / mm['m00'])
                X_angle=cx
                Y_angle=cy
                cv.circle(result, (cx, cy), 3, (0, 0, 255), -1)

            if (p > 250 ):
                if (shape_type == "圆形"):
                    if((math.sqrt(4*area/math.pi)*coefficient[decade])<27):
                        break
                    else:
                        print("直径: %.3f, 中心点: %s 形状: %s " % ( math.sqrt(4*area/math.pi)*coefficient[decade], (cx,cy), shape_type))
                if (shape_type == "矩形"):
                    if(((math.sqrt(area))*coefficient[decade])<25):
                        break
                    print("边长: %.3f,  中心点: %s 形状: %s " % ((math.sqrt(area))*coefficient[decade], (cx,cy), shape_type))
                if (shape_type == "三角形"):
                    if(((math.sqrt(area / (math.sqrt(3) / 4)))*coefficient[decade])<20):
                        break
                    print("边长: %.3f,  中心点: %s 形状: %s " % ((math.sqrt(area / (math.sqrt(3) / 4)))*coefficient[decade],(cx,cy), shape_type))
        
        Distance = 0.0
        print("结束")
        return self.shapes

    def draw_text_info(self, image):
        c1 = self.shapes['triangle']
        c2 = self.shapes['rectangle']
        c3 = self.shapes['polygons']
        c4 = self.shapes['circles']
        cv.putText(image, "triangle: "+str(c1), (10, 20), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv.putText(image, "rectangle: " + str(c2), (10, 40), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv.putText(image, "polygons: " + str(c3), (10, 60), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv.putText(image, "circles: " + str(c4), (10, 80), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        return image

def dis_relay():
    global Distance
    global distance_relay
    distance_relay = Distance

def angle_send():
    global distance_relay
    print(distance_relay)
    x=angle.getangle_x(X_angle-140,distance_relay)
    y=angle.getangle_y(Y_angle-160,distance_relay)
    tmp=str(y)+','+str(x)+',1,1'
    print(tmp)
    ser.write(tmp.encode())
    
while 1:
    while GPIO.input(35) == GPIO.LOW:
        if __name__ == "__main__":
            cut.cut_img()
            sharp.sharp_img()
            src = cv.imread("result.png")
            ld = ShapeAnalysis()
            ld.analysis(src)
            angle_send()
            time.sleep(13)
    
    while GPIO.input(37) == GPIO.LOW:
        if __name__ == "__main__":
            cut.cut_img()
            sharp.sharp_img()
            src = cv.imread("result.png")
            ld = ShapeAnalysis()
            ld.analysis(src)