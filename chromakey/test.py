import cv2
import numpy as np
import sys
import os

dirname = "images/"
filename = "IMG_2679.JPG"

img = cv2.imread(dirname+filename, 1)


width = len(img[1])
height = len(img)

img_B, img_G, img_R = cv2.split(img)

# cv2.imshow("grayB", cv2.resize(img_B, (640,360)))
# cv2.imshow("grayG", cv2.resize(img_G, (640,360)))
# cv2.imshow("grayR", cv2.resize(img_R, (640,360)))

img_aveBR = cv2.addWeighted(img_B, 0.5, img_R, 0.5, 0)
# cv2.imshow("ave", cv2.resize(img_aveBR, (640, 360)))

img_diff = cv2.absdiff(img_G, img_aveBR)
img_diffm = cv2.threshold(img_diff, 55, 150, cv2.THRESH_BINARY)[1]
cv2.imshow("diff", cv2.resize(img_diffm, (640, 360)))

lower_color = np.array([0x00, 0x10, 0x00])
upper_color = np.array([0x80, 0xff, 0x80])

mask = cv2.inRange(img, lower_color, upper_color)
inv_mask = cv2.bitwise_not(img_diffm)
res1 = cv2.bitwise_and(img, img, mask=inv_mask)

print(inv_mask)

out = cv2.bitwise_or(1, res1, img_diffm)

cv2.imshow("out", cv2.resize(out, (640, 360)))
# cv2.imshow("img", cv2.resize(img, (640, 360)))
cv2.waitKey()
cv2.destroyAllWindows()
