import cv2
import os
#import glob
import numpy as np
#from PIL import Image
 
def convertPNG(pngfile,outdir):
    # READ THE DEPTH
    # im_depth = cv2.imread(pngfile)
   
    ##
    # 以灰度模式读取图片
    im_depth = cv2.imread(pngfile,0)
    # 全局直方图均衡化jet2
    img1=cv2.equalizeHist(im_depth)
    # 自适应直方图均衡化
    #clahe=cv.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    #img2=clahe.apply(im_depth)
    
    #apply colormap on depth image(image must be converted to 8-bit per pixel first)
    #im_color=cv2.applyColorMap(cv2.convertScaleAbs(im_depth,alpha=15),cv2.COLORMAP_JET)
    #默认alpha设为1，比设为15效果好
    im_color=cv2.applyColorMap(cv2.convertScaleAbs(img1,alpha=1),cv2.COLORMAP_JET)
    
    return im_color
  
    #convert to mat png
    #im=Image.fromarray(im_color)
    #save image
    #im.save(os.path.join(outdir,os.path.basename(pngfile)))
 
if __name__ == "__main__":
    path = '/data1/GLPDepth/tdepth/'
    path2 = '/data1/GLPDepth/img/'

    file_dir = os.listdir(path)
    for file in file_dir:
        if not os.path.isdir(file):  #需要是绝对路径
            file_name = path + file
            print(file_name)

        (filenum, extension) = os.path.splitext(file)  #去掉文件后缀
        # print(extension) #.tiff
        
        if extension == '.png':
            im_color = convertPNG(file_name,path2)

            cv2.imwrite(path2 + filenum + '.png', im_color)
