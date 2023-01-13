import cv2 as cv
import numpy as np

img = cv.imread('Jennie1.jpg')
ltop = (200, 0)
rtbm = (600, 300)
img_cap = img[ltop[1]:rtbm[1], ltop[0]: rtbm[0]]
img_gray = cv.cvtColor(img_cap, cv.COLOR_BGR2GRAY)
# img_rot=np.rot90(img_gray)
img_flip = cv.flip(img_gray, 1)
cv.imwrite('output.jpg', img_gray)
cv.imshow('Jennie', img_flip)
cv.waitKey(0)