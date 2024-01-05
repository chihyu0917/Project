import cv2
import matplotlib.pyplot as plt
import numpy as np

imagePath = r'./images/lane2.jpg'
image1 = cv2.imread(imagePath)
plt.imshow(image1)

# minimum contour width
min_contour_width = 40  #40

# minimum contour height
min_contour_height = 40  #40
offset = 10   #10
line_height = 550  #550
matches = []
cars = 0

def grey(image):
  #convert to grayscale
    image = np.asarray(image)
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# defining a function
def get_centroid(x, y, w, h):

    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1
    return cx,cy
    # return [cx, cy]

car_cascade = cv2.CascadeClassifier('haarcascade_cars.xml')
copy = np.copy(image1)
greyImg = grey(copy)
cars = car_cascade.detectMultiScale(greyImg, 1.1, 3)
for (x,y,w,h) in cars:
    cv2.rectangle(copy,(x,y),(x+w,y+h),(0,255,0),2)
    crop_img = copy[y:y+h,x:x+w]
cv2.imwrite('outputCars.jpg', copy)
cv2.imshow("cropped", copy)
cv2.waitKey(0)