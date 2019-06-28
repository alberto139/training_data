import cv2
import time
import glob

def main():
    
    video_path = "/home/alberto/Desktop/training_data/out.ogv"
    cap = cv2.VideoCapture(video_path)
    ret, img = cap.read()
    while ret:
        output_path = "/home/alberto/Desktop/training_data/raw_images/" + str(time.time()) + ".png"
        print(output_path)
        cv2.imwrite(output_path, img)
        ret, img = cap.read()

main()