import math

def getangle_x(x,dis):
    dist=dis
    Cx= int((math.atan(x/dist))*57.3)
    if(Cx<0 and Cx>=-10):
        return (Cx-4)
    if(Cx<-10 and Cx>=-20):
        return (Cx-15)
    if(Cx<-20 and Cx>=-30):
        return (Cx-12)
    if(Cx<-30 and Cx>=-40):
        return (Cx-12)
    if(Cx>0 and Cx<=10):
        return (Cx+8)
    if(Cx>10 and Cx<=20):
        return (Cx+10)
    if(Cx>20 and Cx<=30):
        return (Cx+9)
    if(Cx>30 and Cx<=40):
        return (Cx+12)
    
def getangle_y(y,dis):
    dist=dis
    Cy= int((math.atan(y/dist))*57.3)
    if(Cy<0 and Cy>=-10):
        return (Cy-3)
    if(Cy<-10 and Cy>=-20):
        return (Cy-9)
    if(Cy<-20 and Cy>=-30):
        return (Cy-12)
    if(Cy<-30 and Cy>=-40):
        return (Cy-15)
    if(Cy>0 and Cy<=10):
        return (Cy+3)
    if(Cy>10 and Cy<=20):
        return (Cy+6)
    if(Cy>20 and Cy<=30):
        return (Cy+10)
    if(Cy>30 and Cy<=40):
        return (Cy+15)