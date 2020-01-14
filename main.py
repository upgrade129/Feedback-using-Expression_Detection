# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 17:26:37 2020

@author: Admin
"""

def smax(lis,mx):
    if(mx != 0):    
        me = lis[0]
        ind = 0
    else:
        me = lis[1]
        ind = 1
    for i in range(0,len(lis)):
        if(i == mx):
            continue
        if(me < lis[i]):
            me = lis[i]
            ind = i
    return ind
        

import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#img = cv2.imread('/data/friends.jpg')
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #transform image to gray scale
#faces = face_cascade.detectMultiScale(gray, 1.3, 5)
 

from keras.models import model_from_json
model = model_from_json(open("facial_expression_model_structure.json", "r").read())
model.load_weights('facial_expression_model_weights.h5') #load weights

import keras.preprocessing.image as image
import numpy as np

cap = cv2.VideoCapture(0)
 
while(True):
    ret, img = cap.read()
     
    #apply same face detection procedures
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
        detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
        detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48
        img_pixels = image.img_to_array(detected_face)
        img_pixels = np.expand_dims(img_pixels, axis = 0)
         
        img_pixels /= 255
         
        predictions = model.predict(img_pixels)

        #find max indexed array
        max_index = np.argmax(predictions[0])
        
        emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
        emotion = emotions[max_index]
         
        cv2.putText(img, emotion, (int(x+w), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        
        
        smax_index = smax(predictions[0],max_index)
        emotion = emotions[smax_index]         
        cv2.putText(img, emotion, (int(x+w), int(y+50)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        
        cv2.putText(img, str(predictions[0][max_index] - predictions[0][smax_index]),
                    (int(x+w), int(y+100)), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (255,255,255), 2)        
        
        #for i in range(0,7):
            #cv2.putText(img, emotions[i]+"->"+str(predictions[0][i]), (int(x+w), int(y+i*20)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        
        
         
    if cv2.waitKey(1) == ord('q'): #press q to quit
        break
    cv2.imshow('face',img)

cap.release()
cv2.destroyAllWindows()