import cv2  
import matplotlib.pyplot as plt
import csv
import os
import time

path1 = './rawframes/'
tempNum = ''
tempOutPath = ''

font = cv2.FONT_HERSHEY_SIMPLEX
color = (255, 0, 0) 
thickness = 2

with open('annotations/ava_train_v2.2_mini.csv', 'r') as avaData:
    reader = csv.reader(avaData)
    for row in reader:
        if tempNum == row[1]:
            path2 = tempOutPath
        else:
            tempNum = row[1]
            num = str((int(row[1]) - 900) * 30 + 1)
            #print("num",num)
            num = num.zfill(5)
            path2 = path1 + row[0] + '/img_' + num + '.jpg'
        

        image = cv2.imread(path2)         
        sp = image.shape
        h = sp[0]
        w = sp[1]
        
        x1 = int( float(row[2]) * w )
        y1 = int( float(row[3]) * h )
        
        x2 = int( float(row[4]) * w )
        y2 = int( float(row[5]) * h )
        
        start_point = (x1,y1)
        end_point = (x2,y2)
        image = cv2.rectangle(image, start_point, end_point, color, thickness) 
        
        image = cv2.putText(image, row[7], (x1, y1+15), font, 1, (255, 255, 255), 1)
        
        tempOutPath = './out/' + row[0] + '/img_' + num + '.jpg'
        cv2.imwrite(tempOutPath, image)
        if row[0] != '-5KQ66BBWC4':
            break
           #### 图片合成视频
def picvideo(path):
    filelist = os.listdir(path)  # 获取该目录下的所有文件名
    #filelist.sort(key=lambda x: int(x[4:-4]))  ##文件名按数字排序
    '''
    fps:
    帧率：1秒钟有n张图片写进去[控制一张图片停留5秒钟，那就是帧率为1，重复播放这张图片5次] 
    如果文件夹下有50张 534*300的图片，这里设置1秒钟播放5张，那么这个视频的时长就是10秒
    '''
    fps = 10
    file_path = r"./outVideo/5KQ66BBWC4.mp4"  # 导出路径
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')  # 不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）

    image = cv2.imread(path + '/img_00060.jpg') 
    
    sp = image.shape
    
    size = (sp[1],sp[0])
    print(size)
    
    video = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'mp4v'), 2, size)
    print("file_path",file_path)

    for item in filelist:
        if item.endswith('.jpg'):  # 判断图片后缀是否是.png
            item = path  + item
            img = cv2.imread(item)  # 使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。
            video.write(img)  # 把图片写进视频

    video.release()  # 释放

picvideo(r'./out/-5KQ66BBWC4/')

