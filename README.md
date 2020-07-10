# Training Instructions

This repositorie contains step by step instructions on how to train a deep learning model from the TensorFlow object detection zoo. We recomend that you clone this repository and use it as your "home repository" for training. You'll need to have some folders and remember their filepaths so we recomend that you use the same setup as that of this repository.


### Labeling Images
Have a folder with images to be annotated. If you want to annotate a video you must break it down into individual frames. You can do that by using `misc/video2frames.py` in this repository.

Once the images to be annotated are ready, use a labeling tool such as https://github.com/tzutalin/labelImg. This tool requires you clonning the repository and following the installation instructions. 

We focus on labeling:
- Pedestrians (includes: skateboarders, onewheels, unmotorized scooters)
- Cyclists 
- Buses (includes: schools buses, private buses, public buses)
- Cars (includes: pickup trucks, vans)
- Motorcyclist (includes: vespas, motorized scooters)

To label each object use the terms above all in lowercase. When in doubt use your best judgement. Pressing `w` on your keyboard is a shortcut to make a rectangle. Click on the image to place one point of the rectangle. Note that the rectangle only requires 2 points. Make sure to include all of the object within the rectangle. Try to not to have a lot of extra space in the rectange but don't spend to much time on it. Make sure to label of the objects in the image before proceeding to the next. Once all the objects are labelled click the save icon this will generate a `.xml` file that should have the same name as the labeled image.

### Setup Training
The labeled images must be moved around and the .xml files must me converted to a .csv file. The .csv file is then used to create a tf record on which your model will train. 
Most of the setup can be done bby running `python3 setup_training.py`. However you must change the paths to your own. 

---
If you ran `python3 setup_training.py` successfuly you can skip the next 3 steps.

### Move images with labels
Use the `misc/move_images_with_labels.py` to move the labelled images to a seperate folder

### Convert the xml files to csv
Use `misc/xml_to_csv.py`

### Generate tf record
Use `misc/generate_tfrecord.py`
This script requires 2 arguments `--csv_input` and `--output_path`. An example might look like this:
`python3 generate_tfrecord.py --csv_input=/home/alberto/Desktop/data/street_dataset/data/train_labels.csv  --output_path=/home/alberto/Desktop/data/street_dataset/data/train.record`


---

### Download pre-trained model

Download a model from the tensorflow model detection zoo:
`https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md`. For our purpose we recomend ssd_mobilenet_v1_fpn_coco for accuracy or ssd_mobilenet_v1_coco for speed. The dowloaded folder contains the frozen inferece graph and the pipeline.config file. 

### Modify pipeline.config
Once you have downloaded a model you will need to edit the `pipeline.config` file. This is very important and most errors in the training process happen here. 

1. Change `num_classes`
For example if the model was trained on coco num_classes will be 90. In our case we need to change it to 4 (We currently include motorcyclist in cyclist)

2. Change `batch_size`
Most defaul batch sizes are set to 128 or something large. I've found that 32 is much more manageble for older desktop GPUs (GTX 1080). If you have a larger GPU with a lot of RAM you might want to try a larger number.

3. Create a labelmap.pbtxt and replace `label_map_path`
A labelmap file might look like this:
`item {
    id: 1
    name: 'person'
}

item {
    id: 2
    name: 'car'
}

item {
    id: 3
    name: 'cyclist'
}

item {
    id: 4
    name: 'bus'
}`


replace all the instances that read PATH_TO_BE_CONFIGURED after `label_map_path` to the location of your labelmap file.
example: 

4. Replace `fine_tune_checkpoint`
Replace fine_tune_checkpoint: "PATH_TO_BE_CONFIGURED/model.ckpt" with the path to the model checkpoint that you downloaded earlier.
example: fine_tune_checkpoint: "/home/alberto/Desktop/training_data/models/ssd_mobilenet_v1_fpn/model.ckpt"

5. Replace `input_path`
Replace all instances of PATH_TO_BE_CONFIGURED after `input_path` to the path of your tf record file.
example: input_path: "/home/alberto/Desktop/training_data/train.record"


6. Add `from_detection_checkpoint: true`
If there is no line that reads `from_detection_checkpoint: true` you must add that fine after the `fine_tune_checkpoint` line


### Start Training
To train you'll need to have TensorFlow installed and clone the following repository `https://github.com/tensorflow/models`.  We recommend TensorFlow version 1.10.0. This will NOT work with TensorFlow 2.0 

Change directories to models/research

From that directory run `python3 object_detection/legacy/train.py` with the arguments `--train_dir=` and `pipeline_config_path=`. An example might look like this:

`python3 object_detection/legacy/train.py -logstderr --train_dir=/home/alberto/Desktop/data/street_dataset/training_out/ --pipeline_config_path=/home/alberto/Desktop/CurbSpace/models/ssd_mobilenet_v1_fpn/pipeline.config`

`python3 object_detection/legacy/train.py -logstderr --train_dir=/home/alberto/Desktop/training_data/training_out/ --pipeline_config_path=/home/alberto/Desktop/training_data/models/ssd_mobilenet_v1_fpn/pipeline.config`



You can wait until the training ends or you can end it early by pressing ctrl-c.

### Get frozen model
Now that the model is trained we must convert is to a frozen model that we can use later.
from the models/research/object_detection directory run `python3 export_inference_graph.py` with
`--input_type image_tensor`
`--pipeline_config_path`
`--trained_checkpoint_prefix`
`--output_directory`

example:

`
python3 object_detection/export_inference_graph.py --input_type image_tensor --pipeline_config_path /home/alberto/Desktop/Repositories/training_data/models/ssd_mobilenet_v1_fpn/pipeline.config --trained_checkpoint_prefix /home/alberto/Desktop/training_data/training_out/model.ckpt-3611 --output_directory /home/alberto/Desktop/training_data/models/frozen_models
`
---


Lastly: You'll nee to run these commands from the models/research direcotry
`# From tensorflow/models/research/
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
`

`
# If using Tensorflow 1.X:
python object_detection/builders/model_builder_tf1_test.py
`
