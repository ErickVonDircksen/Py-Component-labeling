# Py-Component-labeling
This is a Component Labeling code written in python, it uses some techniques to remove or decrease noise as follow:

Original image: <br>
<img src="150.bmp" width="700" height="500"><br>
Sobel + bilateralFilter <br>
<img src="sobel+BiFilter.png" width="700" height="500"><br>
Treshold OTSU + morphology <br>
<img src="02 -processedImage.png" width="700" height="500"><br>
Final result: <br>
<img src="02 - edgesDetectec.png" width="700" height="500">

The parameters are  very flexible to change, you can  fine tune to adapt better to your images, such as:

<b>cv2.bilateralFilter() <br>
cv2.threshold()<br>
cv2.morphologyEx()<br>
cv2.Canny()<br>
cv2.dilate()</b>

