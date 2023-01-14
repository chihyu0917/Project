import cv2
recognizer = cv2.face.LBPHFaceRecognizer_create()         
recognizer.read('face.yml')                               
cascade_path = "haarcascade_frontalface_default.xml"  
face_cascade = cv2.CascadeClassifier(cascade_path)        
                                
cap = cv2.VideoCapture('./video/Blackpink.mp4')
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, img = cap.read()
    if not ret:
        print("Cannot receive frame")
        break
    # img = cv2.imread('./Blackpink2.jpg')         
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
    faces = face_cascade.detectMultiScale(gray)  

    name = {
        '1':'Jennie',
        '2':'Lisa',
    }

    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)            
        idnum,confidence = recognizer.predict(gray[y:y+h,x:x+w])  
        if confidence < 60:
            text = name[str(idnum)]                               
        else:
            text = '???'                                          
        cv2.putText(img, text, (x,y-5),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

    cv2.imshow('face', img)
    if cv2.waitKey(5) == ord('q'):
        break    
cap.release()
cv2.destroyAllWindows()