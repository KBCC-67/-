import numpy as np
import cv2
ship_img=cv2.imread("ship_item2.png")

new_ship_img=((255-ship_img[:,:,3])/255*ship_img[:,:,0:2]).astype(np.uint8)

cv2.imwrite('newship_item2.png',new_ship_img)
