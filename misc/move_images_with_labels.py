import os
import glob
import shutil



def main(origin_path, output_path):
    print("Moving images...")
    #path = "/mnt/237ddc38-d61e-439b-a72d-09e06eae2f59/images_data/images_caltrans/"

    for filename in glob.glob(origin_path + '*.xml'):
        print(filename[:-4] + ".png") # image file
        image = filename[:-4] + ".png"
        #print(image.split('/')[-1])
        just_the_image_name = image.split('/')[-1]

        
        shutil.copy(filename, output_path)
        shutil.copy(image, output_path + str(just_the_image_name))
        print(filename)
