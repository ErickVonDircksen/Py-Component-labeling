
import cv2
import sys
import matplotlib.pyplot as plt
import numpy as np

path = '150.bmp'

def noNoise2(img):
 img_out = img.copy()
 kernel = np.ones((3,3),np.uint8)

 kernel1 = np.array([[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]], np.uint8)

 mediumPixel = np.average(img)
 print(mediumPixel)

 img_out = cv2.bilateralFilter(img_out, 31,15, 10)
 
 
 
 (a,img_out) = cv2.threshold(img,mediumPixel/2,mediumPixel*2,cv2.THRESH_OTSU) # comentar essa linha faz "funcinar nas imagens diferentes da 150.bmp"

 cv2.imwrite ('02 - Blur+otsu.png', img_out)

 img_out = cv2.adaptiveThreshold(img_out,255,cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,7,14)  

 cv2.imwrite ('03 - Blur+otsu+AdapTative.png', img_out) 

 img_out  = cv2.morphologyEx(img_out,cv2.MORPH_OPEN,kernel,iterations=1) 
 cv2.imwrite ('04 -Blur+otsu+AdapT+Dilated .png', img_out)
 return img_out



image = cv2.imread(path, 0)
if image is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

th3 = noNoise2(image)

canny = cv2.Canny(th3,20, 180, 1)

dilated = cv2.dilate(canny, (2,2), iterations = 1)



(cnt, heirarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.drawContours(rgb, cnt, -1, (0,255,0), 1)

cv2.imwrite ('01 - edgesDetectec.png', rgb)

print('Rice in the image: ', len(cnt))
#cv2.show()

