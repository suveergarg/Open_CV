from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import Tkinter as tk
import math
from itertools import combinations
#input output lists
inp=[]
op=[]
lines=[]
angles=[]

def find_centre(points):
 	x_mean=0
 	y_mean=0		
 	for point in points:
		x,y=point
		x_mean+=x
		y_mean+=y
 	#calculate mean of points
 	return (x_mean/len(points) , y_mean/len(points))

def find_distance(point1,point2):
	x1,y1=point1
	x2,y2=point2
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)
	
def find_slope(point1,point2):
	x1,y1=point1
	x2,y2=point2
	m=(y2-y1)/(x2-x1)
	c=y2-(m*x2)
        return (m,c) 

def find_angle(lines):
	pairs=combinations(lines, 2)
	
	for pair in pairs:
		#print ("Pair:",pair,'\n') 		
		line1,line2= pair	
		m1,c1=line1
		m2,c2=line2
		if(abs(m1*m2) != 1):
			angles.append(math.degrees(math.atan(abs((m2-m1)/(1-abs(m2*m1))))))
		else:
			angles.append(180)

	return (angles)


def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  #for obj in decodedObjects:
    #print('Type : ', obj.type)
    #print('Data : ', obj.data,'\n')
     
  return decodedObjects

# Display barcode and QR code location  
def display(im, decodedObjects):
 
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    	points = decodedObject.location
    	centre=find_centre(points)	
    	#print ("Object:", points,'\n')	    
    	#print ("Centre:", centre, '\n')
    	cv2.circle(im,centre,10,(0,0,255),-1)	   
	cv2.putText(im,decodedObject.data,centre,cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
	#Condition for Input/Output     	
	if (decodedObject.data == '1') :
		#append centre to input 	
		inp.append(centre)
    	else :
		#append centre to output
		op.append(centre);	

  print("Input:",inp)
  print("Output:",op)
  
  for point1 in inp:
	for point2 in op:
		cv2.line(im,point1,point2,(0,0,255))
		#print(find_distance(point1,point2),'\n')		
		cv2.putText(im,str(math.ceil(find_distance(point1,point2))),find_centre([point1,point2]),cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
  		lines.append(find_slope(point1,point2))
  #print (lines)
  if(len(op)<3):
  	print("Angles:",find_angle(lines),'\n');
  #cv2.putText(im,"Angle:"+str(find_angle(lines)),(30,30),cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
  #(h, w) = im.shape[:2]
  #center = (w / 2, h / 2)
  #angle90 = 90	
  #scale = 1.0
  #M = cv2.getRotationMatrix2D(center, angle90, scale)
  #rotated90 = cv2.warpAffine(im, M, (h, w))
  cv2.imshow("Results", im)

def func():
 	print("Hello")
	decodedObjects = decode(im)
    	display(im, decodedObjects)
        
	
image=cv2.imread('TShirt.jpg')
res = cv2.resize(image,None,fx=2.5, fy=2.5, interpolation = cv2.INTER_CUBIC)
im = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
decodedObjects= decode(im)
display(im,decodedObjects)
#cv2.imshow("Results", im)    


while(True):  
 if cv2.waitKey(1) & 0xFF == ord('q'):
	cv2.destroyAllWindows()        
	break

