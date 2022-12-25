import cv2
import numpy as np
import os

path1 = 'C:\\Users\\ouc\\desktop\\suu\\images\\train\\'
path2 = 'C:\\Users\\ouc\\desktop\\suu\\jet2\\train\\'
path = 'C:\\Users\\ouc\\desktop\\suu\\fimg2\\train\\'

file_dir1 = os.listdir(path1)
file_dir2 = os.listdir(path2)
for file1 in file_dir1:
    if not os.path.isdir(file1):  # 需要是绝对路径
        file_name1 = path1 + file1
        file_name2 = path2 + file1
        img1 = cv2.imread(file_name1)
        img2 = cv2.imread(file_name2)
        print(file_name1)

        (filenum, extension) = os.path.splitext(file1)  # 去掉文件后缀
        # print(extension) #.tiff

        if extension == '.png':
            #fimg = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)
            fimg = img1 + img2

            cv2.imwrite(path + filenum + '.png', fimg)

#img1 = cv2.imread("C:\\Users\\ouc\\desktop\\suu\\images\\train\\10000.png")
#img2 = cv2.imread("C:\\Users\\ouc\\desktop\\suu\\jet2\\train\\10000.png")

#fimg = cv2.addWeighted(img1,0.7, img2, 0.3, 0)  #
#fimg = cv2.add(img1,img2)  #2
#fimg = img1+img2  #za

#cv2.imshow('img1',img1)
#cv2.imshow('img2',img2)
#cv2.imshow('fimg',fimg)

#cv2.waitKey(0)
#cv2.destoryAllWindows()