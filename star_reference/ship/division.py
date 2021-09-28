
import cv2
#初始化部分step=img.shape[1]//16
img=cv2.imread("fleet_presence_icons_ps_modified.png")#png也并不保存alpha通道。。。，还是得tga
print(img.shape)
step=32
for i in range(16):
    new_item=img[:,i*step:(i+1)*step]
    print(new_item.shape)
    cv2.imwrite('ship_item'+str(i+1)+'.png',new_item)
    