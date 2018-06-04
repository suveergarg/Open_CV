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
sets=[]
class qr_code(object):
    centre = ()
    data=''
    # The class "constructor" - It's actually an initializer 
    def __init__(self, data,centre):
        self.centre = centre
        self.data = data
        


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
def compute(im, decodedObjects):
  l_sets=[]
  inp=[]
  op=[]		
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    	points = decodedObject.polygon
    	centre=find_centre(points)	
    	#print ("Object:", points,'\n')	    
    	#print ("Centre:", centre, '\n')
	cv2.circle(im,centre,10,(0,0,255),-1)
	cv2.putText(im,decodedObject.data,centre,cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
	#Condition for Input/Output     	
	if (decodedObject.data == '1' or decodedObject.data=='6') :
		#append centre to input 	
		inp.append(qr_code(decodedObject.data,centre))
    	else:
		#append centre to output
		op.append(qr_code(decodedObject.data,centre))	

  #print("Input:",inp)
  #print("Output:",op)
  Threshold=0
  if (len(inp)>1):
  	Threshold= find_distance(inp[0].centre,inp[1].centre)/2  
  	print ("Input pairs:",inp[0].data,inp[1].data)
  
  print ("Threshold:",Threshold)
  for qri in inp:
	val=[]
	for qro in op:
		
		dist=math.ceil(find_distance(qri.centre,qro.centre))
		
		if(dist<Threshold or Threshold==0):			
			val.append(qro)
			#print ("Pairs: " , qri.data,qro.data)		
              		#print ("Dist: " , dist,"\n")
				

		 
	l_sets.append((qri,val))

  for Set in l_sets:
	ip,ops=Set
	print ("Input :", ip.data)
	print ("Output:",  [v.data for v in ops],"\n")
	for op in ops:
		cv2.line(im,ip.centre,op.centre,(0,0,255))
 		cv2.putText(im,str(math.ceil(find_distance(ip.centre,op.centre))),find_centre([ip.centre,op.centre]),cv2.FONT_HERSHEY_SIMPLEX, 1, 255)  
  #lines.append(find_slope(point1,point2))
  #if(len(op)<3):
  #print("Angles:",find_angle(lines),'\n');
  #cv2.putText(im,"Angle:"+str(find_angle(lines)),(30,30),cv2.FONT_HERSHEY_SIMPLEX, 1, 255)				
  

def destroy():
        button.destroy()
        cap.release()
        cv2.destroyAllWindows()	
	button1.destroy()
      

	
#Start of Main Script
root=tk.Tk()
frame=tk.Frame(root)
frame.pack()
button=tk.Button(frame,text="Destroy",command=destroy)
button.pack(side=tk.LEFT)


flag=False
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#res = cv2.resize(image,None,fx=2.5, fy=2.5, interpolation = cv2.INTER_CUBIC)

i=0
while(True):
	root.update()
	ret, frame = cap.read()

   	# Our operations on the frame come here
	im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	decodedObjects= decode(im)
	#print(len(decodedObjects))
	if (len(decodedObjects)>1): 			
		compute(im,decodedObjects)
		
	#display(im)
	cv2.imshow("Results", im)	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
button.destroy()
cap.release()
cv2.destroyAllWindows()
