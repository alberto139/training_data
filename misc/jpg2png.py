
#!/usr/bin/env python
from glob import glob                                                           
import cv2 
pngs = glob('/home/alberto/Desktop/data/street_dataset/images/*.jpg')

for j in pngs:
    img = cv2.imread(j)
    filename = j[:-3] + 'png'
    print(filename)
    cv2.imwrite(filename, img)