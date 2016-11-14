
import cv2
import time
import math

import numpy as np

camera_feed = cv2.VideoCapture(1)
camera_feed.set(cv2.cv.CV_CAP_PROP_FPS, 30)
fps = 30

tframe = cv2.imread('bg.jpg')
avgframe = cv2.imread('bg2.jpg')
i = 1

totspeed = 0
framecount = 0

def nothing(x):
    pass



while(1):
    _,frame = camera_feed.read()
    cv2.flip(frame,1,frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    
    lower = np.array([20,100,100])
    upper = np.array([30,255,255])

    
    mask = cv2.inRange(hsv, lower, upper)

    
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    mask = cv2.erode(mask,element,iterations=2)
    mask = cv2.dilate(mask,element,iterations=2)
    mask = cv2.erode(mask,element)
    
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
     
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        M = cv2.moments(bestContour)
        areaa = M['m00']
        xx = int(M['m10']/areaa)
        yy = int(M['m01']/areaa)  
        cv2.circle(frame, (xx,yy), 3, (0,0,255), 1)
        if i == 1:
        	txx = int(xx)
        	tyy = int(yy)
        	ptime = time.clock()
        	speed = 0
        	i = i+1
        else:
			cv2.line(tframe, (txx,tyy), (xx,yy), (0,0,255), 5)
			ctime = time.clock()
			tdiff = ctime - ptime
			ptime = ctime
			v = math.sqrt((xx-txx)*(xx-txx)+(yy-tyy)*(yy-tyy))
			if tdiff == 0:
				speed = 0
			else:
				#speed = v/tdiff
				#speed = speed*0.00806
				#speed = speed*0.2777
				speed = v*30*0.000264*3.6
        txx = int(xx)
        tyy = int(yy)
        #cv2.putText(frame,str(xx)+ " , " +str(yy), (xx,yy+20),1,1,(0,255,0))
        totspeed = totspeed + speed
        framecount = framecount + 1
        cv2.putText(frame,str(round(speed,2))+ " km/h", (50,50),1,2,(0,0,255))
        #cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 1)
        cv2.circle(frame,(xx,yy),w/2, (0,0,255), 1)
        avgframe = cv2.imread('bg2.jpg')
    else:
        tframe = cv2.imread('bg.jpg')
        i = 1
        if framecount != 0:
        	avgspeed = totspeed/framecount
    		cv2.putText(avgframe,str(round(avgspeed,2))+ " km/h", (10,50),1,2,(0,0,255))
        totspeed = 0
        framecount = 0

    cv2.imshow('track',tframe)
    cv2.moveWindow('track', 710, 50)
    #cv2.imshow('mask',mask)
    #cv2.moveWindow('mask', 710, 50)
    cv2.imshow('frame',frame)
    cv2.moveWindow('frame', 20, 50)
    cv2.imshow('AverageSpeed', avgframe)
    cv2.moveWindow('AverageSpeed', 20, 570)
    
    k = cv2.waitKey(5) & 0xFF
    
    if k == 27:
        break


cv2.destroyAllWindows() 

