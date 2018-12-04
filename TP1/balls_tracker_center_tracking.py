#!/usr/bin/env python

'''
Track a green ball using OpenCV.

    Copyright (C) 2015 Conan Zhao and Simon D. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License 
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import cv2
import numpy as np
import cv


# For OpenCV2 image display
WINDOW_NAME = 'GreenBallTracker' 

color = 'detection' 
height = 0
width = 0
center_img= (0,0)
pixel_table = []
index = 1

def track(image):

    '''Accepts BGR image as Numpy array
       Returns: (x,y) coordinates of centroid if found
                (-1,-1) if no centroid was found
                None if user hit ESC
    '''
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    global index
    sum_h = 0
    sum_s = 0
    sum_v = 0
    
    if index == 1:
      center_array = [center_img,
		      (center_img[0],center_img[1]+1),
		      (center_img[0]+1,center_img[1]+1), 
		      (center_img[0]+1,center_img[1]), 
		      (center_img[0]-1,center_img[1]-1),
	              (center_img[0]-1,center_img[1]),
	              (center_img[0],center_img[1]-1),
	              (center_img[0]-1,center_img[1]+1),
	              (center_img[0]+1,center_img[1]-1)] 

      for i in range(0,len(center_array)):
	px = hsv[center_array[i]]
	pixel_table.append(px)
	

	sum_h = sum_h + pixel_table[i][0] 
	sum_s = sum_s + pixel_table[i][1]
	sum_v = sum_v + pixel_table[i][2]
	
      sum_h = sum_h/len(center_array)
      sum_s = sum_s/len(center_array)
      sum_v = sum_v/len(center_array)
      
      print(sum_h,sum_s,sum_v)
      #print(hsv[center_img])
      if color == 'detection' : 
	lower_array = np.array([sum_h,sum_s,sum_v])
	upper_array = np.array([sum_h+20,200,200])
      
      index+=1
    

    # Threshold the HSV image for only green colors
    if color == 'green' : 
      lower_array = np.array([40,70,70])
      upper_array = np.array([80,200,200])
    
      # Threshold the HSV image for only blue colors
    if color == 'blue' : 
      lower_array = np.array([95,70,70])
      upper_array = np.array([100,200,200])
    
    if color == 'yellow' : 
      lower_array = np.array([27,70,70])
      upper_array = np.array([35,200,200])
      
    if color == 'pink' : 
      lower_array = np.array([160,120,120])
      upper_array = np.array([200,255,255])
      
    if color == 'ball_1' : 
      lower_array = np.array([140,70,70])
      upper_array = np.array([180,200,200])  

    if color == 'detection' : 
	lower_array = np.array([sum_h,sum_s,sum_v])
	upper_array = np.array([sum_h+20,200,200])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_array, upper_array)

    # Blur the mask, Image blurring is achieved by convolving the image with a low-pass filter kernel. It is useful for removing noises
    bmask = cv2.GaussianBlur(mask, (5,5),0)

#technique pour retenir un objet
#on recup

#==================== mon code contour =======================

    #on a capture.read en argument = image, ici on utilise bmask
    contours, hierarchy = cv2.findContours(bmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    showingCNTs = [] # Contours that are visible	
    areas = [] # The areas of the contours

    for cnt in contours:
      approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)

      area = cv2.contourArea(cnt)
      if area > 5000:
	areas.append(area)
	showingCNTs.append(cnt)
				
				## Only Highlight the largest object
    if len(areas)>0:
      m = max(areas)
      maxIndex = 0
      
      for i in range(0, len(areas)):
	if areas[i] == m:
	  maxIndex = i
	  cnt = showingCNTs[maxIndex]
      
      cv2.drawContours(image,[cnt],0,(0,0,255),-1)
   
      x,y,w,h = cv2.boundingRect(cnt)
      cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
      
      center = (x+(w/2),y+(h/2))
      cv2.circle(image,center, 10, (0,0,125), -1)
      
    else : 
      center = (-1,-1)

# ============= d'autre contour et moyen d'entourer ==================

      #rect = cv2.minAreaRect(cnt)
      #box = cv2.cv.BoxPoints(rect)
      #box = np.int0(box)
      #cv2.drawContours(image,[box],0,(0,255,255),2)
      
      
      #(x,y),radius = cv2.minEnclosingCircle(cnt)
      #center = (int(x),int(y))
      #radius = int(radius)
      #cv2.circle(image,center,radius,(255,0,255),2)
      
      
      ## Draw line to center of screen
      #cv2.line(image, (screenMidX, screenMidY), center, (0,0,255),2)

    cv2.imshow(WINDOW_NAME, image)
    return center 

# Test with input from camera
if __name__ == '__main__':

    capture = cv2.VideoCapture('ball2.mp4')
  
    while True:

        okay, image = capture.read()
	height = np.size(image, 0)
	width = np.size(image, 1)
	center_img = ((width /2 ) , (height/2 ) )
	
        if okay:
            if not track(image):
                break
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
           print('Capture failed')
           break

