from math import floor
import cv2
import sys
import numpy as np


# Universidade Tecnológica Federal do Paraná
#===============================================================================
# Alunos Erick H. Dircksen e André L. Gomes

path = '205.bmp'

def noNoise2(img):
 img_out = img.copy()
 kernel = np.ones((3,3),np.uint8)
 ddepth = cv2.CV_16S
 scale = 1
 delta = 0
 mediumPixel = np.average(img)


 img_out = cv2.bilateralFilter(img_out, 37,15, 5)

 grad_x = cv2.Sobel(img_out, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
 grad_y = cv2.Sobel(img_out, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
 abs_grad_x = cv2.convertScaleAbs(grad_x)
 abs_grad_y = cv2.convertScaleAbs(grad_y)
 img_out = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
 #cv2.imwrite ('01 - pós SOBEL.png',img_out)

 (a,img_out) = cv2.threshold(img,mediumPixel/2,mediumPixel*2,cv2.THRESH_OTSU) 

 #img_out = cv2.adaptiveThreshold(img_out,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,9,14)  
 
 (a,img_out) = cv2.threshold(img_out,0,255,cv2.THRESH_BINARY)      

 img_out  = cv2.morphologyEx(img_out,cv2.MORPH_OPEN,kernel,iterations=1) 
 #cv2.imwrite ('02 -processedImage.png', img_out)
 return img_out

def contaContorno(img,cont):
 height = img.shape[1]
 width = img.shape[0]
 contours = 0
 
 for y in range(height):
  for x in range(width):
   b,g,r = (img[x,y])
   if g > 254:
        contours += 1
 
 return floor(contours/cont) 
 

image = cv2.imread(path, 0)
if image is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

deNoised = noNoise2(image)

canny = cv2.Canny(deNoised,30, 160,1,L2gradient=True,apertureSize=7)

dilated = cv2.dilate(canny, (2,2), iterations = 2)

(cnt, hierarchy) = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

cv2.drawContours(rgb, cnt, -1, (0,255,0), 1)

rices = contaContorno(rgb,len(cnt)) 

print("Maybe there is",rices,"rices in",len(cnt),"blobs")

cv2.imwrite ('02 - edgesDetectec.png', rgb)

print()
