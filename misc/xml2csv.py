import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from random import randint

import os
import glob
import shutil


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            filename = root.find('filename').text
            filename = filename[:-3] + 'png'
            value = (filename,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def train_test_split(dataset_path):

    num_in_training = 0
    num_in_testing = 0
    
    print("total files: " + str(2 * len(glob.glob(dataset_path + '*.xml'))))
    for filename in glob.glob(dataset_path + '*.xml'):
        
        num = randint(1,10)
        image = filename[:-4] + ".png"
        just_the_image_name = image.split('/')[-1]

        # Move to train set
        
        if num <= 9:
            shutil.copy(filename, dataset_path + "train/")
            shutil.copy(image, dataset_path + "train/" + str(just_the_image_name))
            num_in_training += 1
        
        # Move to test set
        
        else:
            shutil.copy(filename, dataset_path + "test/")
            shutil.copy(image, dataset_path + "test/" + str(just_the_image_name))
            num_in_testing += 1

    print("Traning: " + str(num_in_training))
    print("testing: " + str(num_in_testing))
    print("Total: " + str(num_in_training + num_in_testing))


def main(xml_path, csv_path):
    # Split into training and testing datasets
    #dataset_path = "/home/alberto/Desktop/data/street_dataset/images/"
    #train_test_split(dataset_path)


    #output_path = "/home/alberto/Desktop/data/street_dataset/data"
    #image_path = origin_path + '{}'.format(directory)
    #image_path = /home/alberto/Desktop/data/street_dataset
    print(xml_path)
    xml_df = xml_to_csv(xml_path)
    #xml_df.to_csv(dataset_path + 'data/{}_labels.csv'.format(directory), index=None)
    xml_df.to_csv(csv_path + '/train_labels.csv', index=None)
    print('Successfully converted xml to csv.')
    #print(output_path + '/{}_labels.csv')

# TODO: Train test split
#main()