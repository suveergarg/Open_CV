from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import Tkinter as tk

def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')
     
  return decodedObjects

# Display barcode and QR code location  
def display(im, decodedObjects):
 
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = decodedObject.location
 
    # If the points do not form a quad, find convex hull
    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points;
     
    # Number of points in the convex hull
    n = len(hull)
 
    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

    cv2.imshow("Results", im)

def func():
 	print("Hello")
	decodedObjects = decode(im)
    	display(im, decodedObjects)
        
	

def destroy():
        button.destroy()
        cap.release()
        cv2.destroyAllWindows()	
	button1.destroy()



root=tk.Tk()
frame=tk.Frame(root)
frame.pack()
button=tk.Button(frame,text="Decode",command=func)
button1=tk.Button(frame,text="Destroy",command=destroy)
button.pack(side=tk.LEFT)
button1.pack(side=tk.LEFT)


flag=False
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

while(True):
    # Capture frame-by-frame
    root.update()
    ret, frame = cap.read()

    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Results", im) 
    
    #if(flag==True):
    	#decodedObjects = decode(im)
    	#display(im, decodedObjects)
        #flag=False   
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
button.destroy()
cap.release()
cv2.destroyAllWindows()
