import cv2
import numpy as np
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  
recog = cv2.face.LBPHFaceRecognizer_create()      
faces = []   
ids = []     

for i in range(1,25):
    img = cv2.imread(f'./face_image/Jennie{i}.jpg')           
    # cv2.imshow('Jennie', img)
    # cv2.waitKey(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    img_np = np.array(gray,'uint8')               
    face = detector.detectMultiScale(gray)        
    for(x,y,w,h) in face:
        faces.append(img_np[y:y+h,x:x+w])         
        ids.append(1)                             

for i in range(1,25):
    img = cv2.imread(f'face_image/Lisa{i}.jpg')          
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    img_np = np.array(gray,'uint8')               
    face = detector.detectMultiScale(gray)        
    for(x,y,w,h) in face:
        faces.append(img_np[y:y+h,x:x+w])         
        ids.append(2)                             

print('Start Training')                              
recog.train(faces,np.array(ids))                  
recog.save('face.yml')                           
print('Finish Training!')