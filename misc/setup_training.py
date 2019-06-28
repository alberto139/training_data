# 1. Label Images
# 2. Move to Desktop/data/street_data/images/ folder
# 3. Covert to xml2csv
# 4. Convert to tf record using generate_tfrecord.py in ~/Desktop/data/street_datset
# python3 generate_tfrecord.py --csv_input=/home/alberto/Desktop/data/street_dataset/data/train_labels.csv  --output_path=/home/alberto/Desktop/data/street_dataset/data/train.record
# python3 generate_tfrecord.py --csv_input=/home/alberto/Desktop/data/street_dataset/data/test_labels.csv  --output_path=/home/alberto/Desktop/data/street_dataset/data/test.record
# 5. Train from ~/models/research
# python object_detection/legacy/train.py -logstderr --train_dir=/home/alberto/Desktop/data/street_dataset/training_out/ --pipeline_config_path=/home/alberto/Desktop/CurbSpace/models/street_sept10/pipeline.config
# 6. Get frzone model
"""
python3 export_inference_graph.py --input_type image_tensor --pipeline_config_path /home/alberto/Desktop/CurbSpace/models/street_sept5/pipeline.config \
    --trained_checkpoint_prefix /home/alberto/Desktop/data/street_dataset/training_out/model.ckpt-200000 \
    --output_directory /home/alberto/Desktop/CurbSpace/models/street_sept5
"""


import xml2csv
import generate_tfrecord
import move_images_with_labels




def main():

    
    train = True
    test = True
    move = True
    xml = True

    # Move image 
    
    if move:
        frames_path = "/home/alberto/Desktop/training_data/raw_images/"
        output_path = "/home/alberto/Desktop/training_data/labelled_images/"
        move_images_with_labels.main(frames_path, output_path)

        print('\n [DONE] moving labeled images \n')

    # xml to csv
    if xml:
        xml_path = "/home/alberto/Desktop/training_data/labelled_images/"
        csv_path = "/home/alberto/Desktop/training_data/"
        xml2csv.main(xml_path, csv_path)

        print("\n [DONE] creating training csv \n")

    # generate tf record
    if train:
        image_paths = "/home/alberto/Desktop/training_data/labelled_images"
        csv_input = "/home/alberto/Desktop/training_data/train_labels.csv"  
        output_path = "/home/alberto/Desktop/training_data/train.record"
        generate_tfrecord.main(image_paths, csv_input, output_path)

        print("\n [DONE] generating tf record \n")

    #if test:
    #    images_input = "/home/alberto/Desktop/data/street_dataset/images"
    #    csv_input = "/home/alberto/Desktop/data/street_dataset/data/test_labels.csv"  
    #    output_path = "/home/alberto/Desktop/data/street_dataset/data/test.record"
    #    generate_tf_record.main(images_input, csv_input, output_path)


main()