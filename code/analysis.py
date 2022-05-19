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
GPIO.setup(33, GPIO.IN)

ser = serial.Serial('/dev/ttyS0', 9600,timeout=10)
coefficient = [0.3097,0.3241,0.3365,0.3517,0.3645,0.3825,0.3954,0.4093,0.4268,0.4457,0.4695,0.4877,0.5077,0.5287,0.5287,0.5287,0.5287,0.5287,0.5287,0.5287,0.5287,0.5287,0.5287,0.5287,0.5287,0.5287]

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
    ser.flushInput()
    tmp_start='0,0,0,0,1'
    ser.write(tmp_start.encode())
    data = ser.read(90)
    time.sleep(2)
    ser.flushInput()
    #print(data)
    str_num=(re.findall(r"\d+\.?\d",data.decode('utf-8')))
    #print(str_num)
    long = len(str_num)
    for num in range(0,long):
        if(float(str_num[num])>150 and float(str_num[num])<350):
            all += float(str_num[num])
            tmp+=1
            #print(tmp,all)
    Distance=all/tmp
    #print("距离"+"%.2f"%(Distance))
    flag=0
    if (Distance>200):
        flag=Distance-200
    if (Distance<200):
        flag=200-Distance
    decade = int(flag /10)
    #print(decade)
    tmp = 0
    dis_relay()
    Distance =0.0

def distance_ball():
    global tmp
    all = 0.0
    global Distance
    global decade
    ser.flushInput()
    tmp_start='0,0,0,0,1'
    ser.write(tmp_start.encode())
    data = ser.read(90)
    time.sleep(2)
    ser.flushInput()
    #print(data)
    str_num=(re.findall(r"\d+\.?\d",data.decode('utf-8')))
    #print(str_num)
    long = len(str_num)
    for num in range(0,long):
        if(float(str_num[num])>150 and float(str_num[num])<350):
            all += float(str_num[num])
            tmp+=1
            #print(tmp,all)
    Distance=all/tmp
    #print("距离"+"%.2f"%(Distance))
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
        #print("start ")
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        
        distance()
        #print("距离"+"%.2f"%(distance_relay+5))
        
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
                shape_type = "正方形"
            if corners >= 10:
                count = self.shapes['circles']
                count = count + 1
                self.shapes['circles'] = count
                shape_type = "圆形"
            if 4 < corners < 10:
                count = self.shapes['polygons']
                count = count + 1
                self.shapes['polygons'] = count
                shape_type = "正方形"


            global X_angle
            global Y_angle

            p = cv.arcLength(contours[cnt], True)
            area = cv.contourArea(contours[cnt])

            if(p>200):
                mm = cv.moments(contours[cnt])
                cx = int(mm['m10'] / mm['m00'])
                cy = int(mm['m01'] / mm['m00'])
                X_angle=cx
                Y_angle=cy
                cv.circle(result, (cx, cy), 3, (0, 0, 255), -1)

            if (p > 200 ):
                if (shape_type == "圆形"):
                    if((math.sqrt(4*area/math.pi)*coefficient[decade])<28):
                        continue
                    else:
                        print("直径: %.3f, 中心点: %s 形状: %s " % ( math.sqrt(4*area/math.pi)*coefficient[decade], (cx,cy), shape_type))
                if (shape_type == "正方形"):
                    if(((math.sqrt(area))*coefficient[decade])<26 and ((math.sqrt(area))*coefficient[decade]) > 15):
                        print("边长: %.3f,  中心点: %s 形状: 三角形 " % ((math.sqrt(area / (math.sqrt(3) / 4)))*coefficient[decade], (cx,cy)))
                    else:
                        print("边长: %.3f,  中心点: %s 形状: %s " % ((math.sqrt(area))*coefficient[decade], (cx,cy), shape_type))
                if (shape_type == "三角形"):
                    if(((math.sqrt(area / (math.sqrt(3) / 4)))*coefficient[decade])<20):
                        continue
                    print("边长: %.3f,  中心点: %s 形状: %s " % ((math.sqrt(area / (math.sqrt(3) / 4)))*coefficient[decade],(cx,cy), shape_type))
        
        Distance = 0.0
        
        return self.shapes

    def analysis_ball(self, frame):
        h, w, ch = frame.shape
        global coefficient
        global Distance
        result = np.zeros((h, w, ch), dtype=np.uint8)
        #print("start\n")
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        
        distance_ball()
        football =0
        basketball = 0
        volleyball = 0
        contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        #print("start")
        for cnt in range(len(contours)):
            cv.drawContours(result, contours, cnt, (0, 255, 0), 2)

            global X_angle
            global Y_angle

            p = cv.arcLength(contours[cnt], True)
            area = cv.contourArea(contours[cnt])
            if(p>30):
                mm = cv.moments(contours[cnt])
                cx = int(mm['m10'] / mm['m00'])
                cy = int(mm['m01'] / mm['m00'])
                X_angle=cx
                Y_angle=cy
                cv.circle(result, (cx, cy), 3, (0, 0, 255), -1)
                color = frame[cy][cx]
                #print(cx, cy)
                color_str = "(" + str(color[0]) + ", " + str(color[1]) + ", " + str(color[2]) + ")"
                #print(color_str)
                b,g,r =np.transpose(color)[0],np.transpose(color)[1],np.transpose(color)[2]
                b,g,r =int(b),int(g),int(r)
                #print(r,g,b)

                if(r+g+b<255 or r+g+b>550):
                    football +=1
                elif(r>=(g+b)/2):
                    basketball +=1
                else:
                    volleyball +=1
                
        if(basketball>football and basketball > volleyball):
            print("篮球")
        elif(football>basketball and football >=volleyball):
            print("足球")
        else:
            print("排球")
        #print(basketball,football,volleyball)
        football =0
        basketball = 0
        volleyball = 0
        gougu=math.sqrt((cx-140)**2+(cy-140)**2)
        dis_ball= math.sqrt((gougu*coefficient[decade])**2+(distance_relay)**2)
        print("距离 : "+"%.2f" % (dis_ball-11))

        Distance = 0.0
        return self.shapes


def finish_light():
    tmp_end='0,0,0,1,0'
    #print(tmp_end)
    ser.write(tmp_end.encode())

def dis_relay():
    global Distance
    global distance_relay
    distance_relay = Distance

def angle_send():
    global distance_relay
    global coefficient
    #print(distance_relay)
    x=angle.getangle_x(X_angle-152,distance_relay)
    y=angle.getangle_y(Y_angle-164,distance_relay)
    tmp2=str(y)+','+str(x)+',1,1,0'
    #print(tmp2)
    gougu=math.sqrt((X_angle-140)**2+(Y_angle-140)**2)
    dis_ball= math.sqrt((gougu*coefficient[decade])**2+(distance_relay+5)**2)
    print("距离 : "+"%.2f" % (dis_ball))
    ser.write(tmp2.encode())

def angle_send_ball():
    global distance_relay
    #print(distance_relay)
    x=angle.getangle_x(X_angle-120,distance_relay)
    y=angle.getangle_y(Y_angle-120,distance_relay)
    tmp2=str(y)+','+str(x)+',1,1,0'
    #print(tmp2)
    ser.write(tmp2.encode())
    

while 1:
    while GPIO.input(35) == GPIO.LOW:
        if __name__ == "__main__":
            print("识别开始：\n")
            cut.cut_img()
            sharp.sharp_img()
            src = cv.imread("result.png")
            ld = ShapeAnalysis()
            ld.analysis(src)
            angle_send()
            print("结束")
            time.sleep(5)
            ser.flushInput()
            print("\n")

    while GPIO.input(37) == GPIO.LOW:
        if __name__ == "__main__":
            print("识别开始：\n")
            cut.cut_img()
            sharp.sharp_img()
            src = cv.imread("result.png")
            ld = ShapeAnalysis()
            ld.analysis(src)
            ser.flushInput()
            print("距离 : "+"%.2f" % (distance_relay+4))
            print("结束")
            finish_light()
            print("\n")

    while GPIO.input(33) == GPIO.LOW:
        if __name__ == "__main__":
            print("识别开始：\n")
            cut.cut_ball()
            sharp.sharp_ball()
            src = cv.imread("result.png")
            ld = ShapeAnalysis()
            ld.analysis_ball(src)
            angle_send_ball()
            print("结束")
            time.sleep(5)
            print("\n")