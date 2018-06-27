import numpy as np
import cv2


upperbody_cascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')

cap = cv2.VideoCapture(0)
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected = upperbody_cascade.detectMultiScale(gray, 1.3, 5)
    height,width=gray.shape
    roi_gray = np.zeros((height, width), np.uint8)	
    for (x,y,w,h) in detected:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray[y+(h/2):y+h, x:x+w] = gray[y+(h/2):y+h, x:x+w]
        
    outline = cv2.Canny(roi_gray,100,200)
    outline1 = cv2.Canny(gray,100,200)	    
    cv2.imshow('Using Classifier :Only Shoulder',outline)
    cv2.imshow('Only Edge Detection',outline1)	    
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
