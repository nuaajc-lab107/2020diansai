 # -*- coding: utf-8 -*
import cv2 as cv
import time

def cut_img():
    video_caputre = cv.VideoCapture(0)
    fps = video_caputre.get(cv.CAP_PROP_FPS)
    width = video_caputre.get(cv.CAP_PROP_FRAME_WIDTH)
    height = video_caputre.get(cv.CAP_PROP_FRAME_HEIGHT)
    if(fps==0):
        video_caputre = cv.VideoCapture(1)
        fps = video_caputre.get(cv.CAP_PROP_FPS)
        width = video_caputre.get(cv.CAP_PROP_FRAME_WIDTH)
        height = video_caputre.get(cv.CAP_PROP_FRAME_HEIGHT)
    #print("fps:", fps)
    #print("width:", width)
    #print("height:", height)
    
    size = (int(height/2), int(width / 2))
    #print(size)
    
    videp_write = cv.VideoWriter("videoFrameTarget001.avi", cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
    success, frame_src = video_caputre.read()
    success2, frame_src2 = video_caputre.read()
    cv.imwrite('cut1.png',frame_src2)
    success3, frame_src3 = video_caputre.read()
    tmp=frame_src
    cv.imwrite('cut2.png',frame_src3)
    local_time=time.time()
    while success and True:
        frame_target = frame_src[100:380, 180:460]
        # videp_write.write(frame_target)
        success, frame_src_final = video_caputre.read()
        frame_final = frame_src_final[100:380, 180:460]
        cv.imwrite("cut.png", frame_final)
        #cv.imshow("Video_src", frame_src)
        tmp =time.time()
        if tmp-local_time>=3:
            break

        
    #print("视频裁剪完成")
    #cv.destroyWindow("video")
    #cv.destroyWindow("Video_src")
    video_caputre.release()

def cut_ball():
    video_caputre = cv.VideoCapture(0)
    fps = video_caputre.get(cv.CAP_PROP_FPS)
    width = video_caputre.get(cv.CAP_PROP_FRAME_WIDTH)
    height = video_caputre.get(cv.CAP_PROP_FRAME_HEIGHT)
    if(fps==0):
        video_caputre = cv.VideoCapture(1)
        fps = video_caputre.get(cv.CAP_PROP_FPS)
        width = video_caputre.get(cv.CAP_PROP_FRAME_WIDTH)
        height = video_caputre.get(cv.CAP_PROP_FRAME_HEIGHT)
    #print("fps:", fps)
    #print("width:", width)
    #print("height:", height)
    
    size = (int(height/2), int(width / 2))
    #print(size)
    
    videp_write = cv.VideoWriter("videoFrameTarget001.avi", cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
    success, frame_src = video_caputre.read()
    local_time=time.time()
    while success and True:
        frame_target = frame_src[130:350, 210:430]
        success, frame_src_final = video_caputre.read()
        frame_final = frame_src_final[130:350, 210:430]
        cv.imwrite("cut.png", frame_final)
        tmp =time.time()
        if tmp-local_time>=3:
            break

    #print("视频裁剪完成")
    video_caputre.release()

if __name__ == "__main__":
    cut_img()