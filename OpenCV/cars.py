import cv2
img = cv2.imread('cars.jpg')                    # 讀取街道影像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # 轉換成黑白影像

car = cv2.CascadeClassifier("cars.xml")    # 讀取汽車模型
gray = cv2.medianBlur(gray, 5)                  # 模糊化去除雜訊
cars = car.detectMultiScale(gray, 1.1, 3)       # 偵測汽車
cars_num = 0
for (x, y, w, h) in cars:
    cars_num += 1
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)   # 繪製外框

print(cars_num)
cv2.imshow('cars', img)
cv2.waitKey(0) # 按下任意鍵停止
cv2.destroyAllWindows()