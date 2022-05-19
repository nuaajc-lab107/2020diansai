import math

def getangle_x(x,dis):
    dist=dis
    Cx= int((math.atan(x/dist))*57.3)
    return (Cx)

def getangle_y(y,dis):
    dist=dis
    Cy= int((math.atan(y/dist))*57.3)
    return (Cy)