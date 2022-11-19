# --*-- coding:utf-8 --*--
import math
import cv2
import os
import math

from utils.rgbd_util import *
from utils.getCameraParam import *

'''
must use 'COLOR_BGR2GRAY' here, or you will get a different gray-value with what MATLAB gets.
'''
def getImage(file_name):
    
    D = cv2.imread( file_name , cv2.COLOR_BGR2GRAY)
    ##改为除以最大值？
    M = np.max(D)
    D = D/M
    # 海参灰度图最大值为47751，需要除以10000。最后单位需要是m，可能得除以100000。后面转rgb会乘100。
    # 改为除以50000，后面乘255，视觉效果更好。
    RD = D
    # RD = cv2.imread(os.path.join(root, '0_raw.png'), cv2.COLOR_BGR2GRAY)/10000
    return D, RD

'''
C: Camera matrix
D: Depth image, the unit of each element in it is "meter"
RD: Raw depth image, the unit of each element in it is "meter"
'''
def getHHA(C, D, RD):
    missingMask = (RD == 0);
    # pc, N, yDir, h, pcRot, NRot = processDepthImage(D * 100, missingMask, C);
    pc, N, yDir, h, pcRot, NRot = processDepthImage(D * 255, missingMask, C);
    
    tmp = np.multiply(N, yDir)
    acosValue = np.minimum(1,np.maximum(-1,np.sum(tmp, axis=2)))
    angle = np.array([math.degrees(math.acos(x)) for x in acosValue.flatten()])
    angle = np.reshape(angle, h.shape)

    '''
    Must convert nan to 180 as the MATLAB program actually does. 
    Or we will get a HHA image whose border region is different
    with that of MATLAB program's output.
    '''
    angle[np.isnan(angle)] = 180        


    pc[:,:,2] = np.maximum(pc[:,:,2], 100)
    I = np.zeros(pc.shape)

    # opencv-python save the picture in BGR order.
    I[:,:,2] = 31000/pc[:,:,2]
    I[:,:,1] = h
    I[:,:,0] = (angle + 128-90)

    # print(np.isnan(angle))

    '''
    np.uint8 seems to use 'floor', but in matlab, it seems to use 'round'.
    So I convert it to integer myself.
    '''
    I = np.rint(I)

    # np.uint8: 256->1, but in MATLAB, uint8: 256->255
    I[I>255] = 255
    HHA = I.astype(np.uint8)
    return HHA

if __name__ == "__main__":
    path = '/Users/Vita/Desktop/SfM/8.8 depth/'
    path2 = '/Users/Vita/PycharmProjects/Depth2HHA-python-master/img/'

    file_dir = os.listdir(path)
    for file in file_dir:
        if not os.path.isdir(file):  #需要是绝对路径
            file_name = path + file
            print(file_name)

        (filenum, extension) = os.path.splitext(file)  #去掉文件后缀
        # print(extension) #.tiff

        if extension == '.tiff':
            (filenum, extension) = os.path.splitext(filenum)  #去掉文件后缀

            D, RD = getImage(file_name)
            camera_matrix = getCameraParam('color')
            #print('max gray value: ', np.max(D))        # make sure that the image is in 'meter'
            hha = getHHA(camera_matrix, D, RD)
            #hha_complete = getHHA(camera_matrix, D, D)
            cv2.imwrite(path2 + filenum + '.png', hha)
            #cv2.imwrite('demo/hha_complete.png', hha_complete)

