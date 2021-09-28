import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import math as m
#初始化部分
star_name_file=open("Ancient_Chinese_Stellaris.txt","r")
star_names=list()
for line in star_name_file:
    name=line.strip('\n')
    star_names.append(name)
name_num=len(star_names)

nwptu_ship_name_file=open("NWPU_ship_names.txt")
nwptu_ship_names=list()
for line in nwptu_ship_name_file:
    name_line=line.strip('\n')
    names=name_line.split(' ')
    for name in names:
        nwptu_ship_names.append(name)
nwptu_name_num=len(nwptu_ship_names)

show_canvas=np.zeros((1024,1536,3),dtype=np.uint8)
#show_canvas=cv2.imread('star_reference/nebulai2.png')
#show_canvas=cv2.resize(show_canvas,(show_canvas.shape[1]//2,show_canvas.shape[0]//2))
cv2.imwrite("canvas.png",show_canvas)
######################################################################################
#函数部分
def merge(graph,adding,x,y):
    graph=graph.astype(np.uint16)
    cv2.imwrite('tmp_pointer.png',adding)
    try:
        graph[y:y+adding.shape[0],x:x+adding.shape[1]]=graph[y:y+adding.shape[0],x:x+adding.shape[1]]+adding
    except:
        print('unable to comply')
    ret,graph[:,:,0]=cv2.threshold(graph[:,:,0], 255, 255, cv2.THRESH_TRUNC)
    ret,graph[:,:,1]=cv2.threshold(graph[:,:,1], 255, 255, cv2.THRESH_TRUNC)
    ret,graph[:,:,2]=cv2.threshold(graph[:,:,2], 255, 255, cv2.THRESH_TRUNC)
    graph=graph.astype(np.uint8)
    return graph
def new_putText(graph,star_name,position,color,font_size=25):
    img_PIL = Image.fromarray(cv2.cvtColor(graph, cv2.COLOR_BGR2RGB))
    font = ImageFont.truetype('msyh.ttc', font_size)
    draw = ImageDraw.Draw(img_PIL)
    color_0=color[2]
    color_1=color[1]
    color_2=color[0]
    draw.text(position, star_name, font=font, fill=(color_0,color_1,color_2))
    img_OpenCV = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img_OpenCV
def initialize_a_star(pos_x,pos_y):
    x=pos_x#x坐标
    y=pos_y#y坐标
    size=random.uniform(1.0,2.1)#+speed/5
    star_type=random.randint(1,15)
    name_index=random.randint(0,name_num-1)
    name=star_names[name_index]
    star_vec=list([x,y,size,star_type,name])
    return star_vec
def initialize_a_ship(pos_x,pos_y,owner):
    x=pos_x#x坐标
    y=pos_y#y坐标
    size=5
    ship_type=owner
    ship_index=random.randint(0,999)
    if owner==1:
        name="XDV-"+str(ship_index)
    elif owner==2:
        name="NPV-"+nwptu_ship_names[random.randint(0,nwptu_name_num)]
    elif owner==3:
        ship_id=random.randint(0,25)
        name="KHS-"+chr(ship_id+ord('A'))+str(ship_index)
    ship_vec=list([x,y,size,ship_type,name])
    return ship_vec
def draw_star(x,y,size,star_type,star_name,graph,owner):
    op=0
    reference=cv2.imread("star_reference/"+str(star_type)+".jpg")
    reference=cv2.resize(reference,(int(reference.shape[0]/8*size+1),int(reference.shape[1]/8*size+1)))#亮度改成用来变星星大小，加一用来防止变成0
    #cv2.imwrite("test.jpg",reference)引用图片获取没有问题
    r_y=reference.shape[0]
    r_x=reference.shape[1]
    try:
        graph=graph.astype(np.uint16)#变过去，三个通道分别门限二值化再变回来，这样就不会有加法溢出的问题了
            #二值化只能用于单通道图像，所以三个分别搞
        graph[int(y)-int(r_y/2):int(y)-int(r_y/2)+r_y,int(x)-int(r_x/2):int(x)-int(r_x/2)+r_x]=graph[int(y)-int(r_y/2):int(y)-int(r_y/2)+r_y,int(x)-int(r_x/2):int(x)-int(r_x/2)+r_x]+reference
        ret,graph[:,:,0]=cv2.threshold(graph[:,:,0], 255, 255, cv2.THRESH_TRUNC)
        ret,graph[:,:,1]=cv2.threshold(graph[:,:,1], 255, 255, cv2.THRESH_TRUNC)
        ret,graph[:,:,2]=cv2.threshold(graph[:,:,2], 255, 255, cv2.THRESH_TRUNC)
        graph=graph.astype(np.uint8)
        if owner==1:
            color=(100,235,0)
        elif owner==2:
            color=(235,120,255)
        elif owner==3:
            color=(0,0,255)
        position=(int(x), int(y-5))
        graph=new_putText(graph,star_name,position,color)
    #上面巨长的这一行，上限都是减完再加回去，这样保证切片大小正好等于引用素材的大小
    except:
        op=1#这样画不上去就自动退出，也不影响
        print("unsuccessful operation:",x,y,r_y,r_x)#最后发现第一张之后全画不上去是因为x y坐标变成浮点数了。。。。。。草
    return op,graph
def draw_ship(x,y,size,ship_item,star_name,graph,owner):
    op=0
    if owner==1:
        reference=cv2.imread("items/ship_item1.png")
    elif owner==2:
        reference=cv2.imread("items/ship_item_nwptu.png")
    elif owner==3:
        reference=cv2.imread("items/ship_item4.png")
    reference=cv2.resize(reference,(int(reference.shape[0]/4*size+1),int(reference.shape[1]/4*size+1)))#亮度改成用来变星星大小，加一用来防止变成0
    #cv2.imwrite("test.jpg",reference)#引用图片获取没有问题
    r_y=reference.shape[0]
    r_x=reference.shape[1]
    try:
        graph=graph.astype(np.uint16)#变过去，三个通道分别门限二值化再变回来，这样就不会有加法溢出的问题了
            #二值化只能用于单通道图像，所以三个分别搞
        graph[int(y)-int(r_y/2):int(y)-int(r_y/2)+r_y,int(x)-int(r_x/2):int(x)-int(r_x/2)+r_x]=graph[int(y)-int(r_y/2):int(y)-int(r_y/2)+r_y,int(x)-int(r_x/2):int(x)-int(r_x/2)+r_x]+reference
        ret,graph[:,:,0]=cv2.threshold(graph[:,:,0], 255, 255, cv2.THRESH_TRUNC)
        ret,graph[:,:,1]=cv2.threshold(graph[:,:,1], 255, 255, cv2.THRESH_TRUNC)
        ret,graph[:,:,2]=cv2.threshold(graph[:,:,2], 255, 255, cv2.THRESH_TRUNC)
        graph=graph.astype(np.uint8)
        if owner==1:
            color=(100,235,0)
        elif owner==2:
            color=(235,120,255)
        elif owner==3:
            color=(0,0,255)
        position=(int(x+15), int(y-5))
        graph=new_putText(graph,star_name,position,color,15)
    #上面巨长的这一行，上限都是减完再加回去，这样保证切片大小正好等于引用素材的大小
    except:
        op=1#这样画不上去就自动退出，也不影响
        print("unsuccessful operation:",x,y,r_y,r_x)#最后发现第一张之后全画不上去是因为x y坐标变成浮点数了。。。。。。草
    return op,graph
def RightClickDetected(event):
    RX.set(event.x)
    RY.set(event.y)
    return 0
def rotate(image, angle, center=None, scale=1.0):  # 1
    (h, w) = image.shape[:2]  # 2
    if center is None:  # 3
        center = (w // 2, h // 2)  # 4

    M = cv2.getRotationMatrix2D(center, angle, scale)  # 5

    rotated = cv2.warpAffine(image, M, (w, h))  # 6
    return rotated  # 7
def draw_pointer(start_x,start_y,end_x,end_y,owner,crt_canvas):
    if owner==1:
        pointer_img=cv2.imread('items/pointer_green.png')
    if owner==2:
        pointer_img=cv2.imread('items/pointer_pink.png')
    if owner==3:
        pointer_img=cv2.imread('items/pointer_red.png')
    dx=end_x-start_x
    if dx==0:
        dx=1#防止除法bug
    dy=end_y-start_y
    rotation_angle=m.atan(-dy/dx)/m.pi*180#measures in angle
    rotated_pointer=rotate(pointer_img,rotation_angle)
    if dx<0:
        rotated_pointer=cv2.flip(rotated_pointer,-1)
    rotated_pointer=cv2.resize(rotated_pointer,(int(rotated_pointer.shape[0]/8+1),int(rotated_pointer.shape[1]/8+1)))
    #旋转之后贴在用户点的两个点之间正中间就完事了
    center_x=int(start_x+dx/2)
    center_y=int(start_y+dy/2)
    merge_start_x=center_x-rotated_pointer.shape[1]//2
    merge_start_y=center_y-rotated_pointer.shape[0]//2
    print(crt_canvas.shape,rotated_pointer.shape,merge_start_x,merge_start_y)
    new_canvas=merge(crt_canvas,rotated_pointer,merge_start_x,merge_start_y)
    return new_canvas
def clickDetected(event):#太神奇了，event自动获取左键点击,但是太神奇了导致没法往里加别的参数 。。所以画的图还得从外面现场再读取一次
    X.set(event.x)
    Y.set(event.y)
    crt_graph=cv2.imread("canvas.png")
    print("点击位置：",event.x,event.y)
    if what.get()==1:
        crt_star_vec=initialize_a_star(event.x,event.y)
        op_ref,new_graph=draw_star(crt_star_vec[0],crt_star_vec[1],crt_star_vec[2],crt_star_vec[3],crt_star_vec[4],crt_graph,1)
    if what.get()==10:
        crt_star_vec=initialize_a_star(event.x,event.y)
        op_ref,new_graph=draw_star(crt_star_vec[0],crt_star_vec[1],crt_star_vec[2],crt_star_vec[3],crt_star_vec[4],crt_graph,2)
    if what.get()==11:
        crt_star_vec=initialize_a_star(event.x,event.y)
        op_ref,new_graph=draw_star(crt_star_vec[0],crt_star_vec[1],crt_star_vec[2],crt_star_vec[3],crt_star_vec[4],crt_graph,3)
    if what.get()==2:
        print('here')#莫名其妙的，今天这个print都没反应了
        addition_item=cv2.imread('items/xdu.png')
        new_graph=merge(crt_graph,addition_item,event.x,event.y)#咱的函数不是inplace的！！！你得赋值才能用！
    if what.get()==3:
        addition_item=cv2.imread('items/nwptu.png')
        new_graph=merge(crt_graph,addition_item,event.x,event.y)
    if what.get()==4:
        crt_star_vec=initialize_a_ship(event.x,event.y,1)
        op_ref,new_graph=draw_ship(crt_star_vec[0],crt_star_vec[1],crt_star_vec[2],crt_star_vec[3],crt_star_vec[4],crt_graph,1)
    if what.get()==5:
        crt_star_vec=initialize_a_ship(event.x,event.y,2)
        op_ref,new_graph=draw_ship(crt_star_vec[0],crt_star_vec[1],crt_star_vec[2],crt_star_vec[3],crt_star_vec[4],crt_graph,2)
    if what.get()==6:
        crt_star_vec=initialize_a_ship(event.x,event.y,3)
        op_ref,new_graph=draw_ship(crt_star_vec[0],crt_star_vec[1],crt_star_vec[2],crt_star_vec[3],crt_star_vec[4],crt_graph,3)
    if what.get()==7:
        new_graph=draw_pointer(RX.get(),RY.get(),event.x,event.y,1,crt_graph)
    if what.get()==8:
        new_graph=draw_pointer(RX.get(),RY.get(),event.x,event.y,2,crt_graph)
    if what.get()==9:
        new_graph=draw_pointer(RX.get(),RY.get(),event.x,event.y,3,crt_graph)
    cv2.imwrite("canvas.png",new_graph)
    #root.update()#刷新不出来
    new_graph_PIL = Image.fromarray(cv2.cvtColor(new_graph, cv2.COLOR_BGR2RGB))#先转隔壁PIL
    struct_img = ImageTk.PhotoImage(image = new_graph_PIL)#再转专门的tk格式
    theLabel.configure(image = struct_img)#然后这两个才能给更新Label里的图片
    theLabel.image=struct_img
    return 0
######################################################################################
#界面的程序
#root = tk.Tk()#第一次运行用这个，之后都用下面那一行Toplevel这样就不会报错
root = tk.Toplevel()
root.title('星际战役编辑器')
#状态变量
what = tk.IntVar(value=1)
#记录鼠标位置的变量
X = tk.IntVar(value=0)
Y = tk.IntVar(value=0)
RX = tk.IntVar(value=100)#给右键位置用的，只给箭头绘制用来存储箭头初始位置
RY = tk.IntVar(value=100)
#颜色
color_var=tk.IntVar(value=0)
#菜单
menuType = tk.Menu(root, tearoff=0)
def drawStar():
    what.set(1)
menuType.add_command(label='西电星空天体', command=drawStar)
def drawStar():
    what.set(10)
menuType.add_command(label='瓜大星空天体', command=drawStar)
def drawStar():
    what.set(11)
menuType.add_command(label='敌对星空天体', command=drawStar)
def addBg():
    what.set(2)
menuType.add_command(label='西电校徽', command=addBg)
def matrixMerge():
    what.set(3)
menuType.add_command(label='西工大校徽', command=matrixMerge)
def drawShip():
    what.set(4)
menuType.add_command(label='西电舰船', command=drawShip)
def drawShip_2():
    what.set(5)
menuType.add_command(label='西工大舰船', command=drawShip_2)
def drawShip_3():
    what.set(6)
menuType.add_command(label='敌对舰船', command=drawShip_3)
def drawPointer():
    what.set(7)
menuType.add_command(label='绿色箭头', command=drawPointer)
def drawPointer_2():
    what.set(8)
menuType.add_command(label='粉色箭头', command=drawPointer_2)
def drawPointer_3():
    what.set(9)
menuType.add_command(label='红色箭头', command=drawPointer_3)
root.config(menu=menuType)#显示菜单
root.bind("<Button-1>",clickDetected)#鼠标点击事件 button2是滚轮键，button3是右键，不写button是鼠标移动就触发
root.bind("<Button-3>",RightClickDetected)
#增加背景图片
photo = tk.PhotoImage(file="canvas.png")
theLabel = tk.Label(root,
                    text="",#内容
                    justify=tk.LEFT,#对齐方式
                    image=photo,#加入图片
                    compound = tk.CENTER,#关键:设置为背景图片
                    font=("华文行楷",20),#字体和字号
                    fg = "white")#前景色
theLabel.pack()

 

tk.mainloop()