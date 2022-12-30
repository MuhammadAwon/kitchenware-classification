# Kitchenware Classification with TensorFlow Lite

Developing and productization of a Machine Learning model for classification of six kitchen utensils.

The client app is build to classify images of kitchware items using Tensorflow Lite model from the following classes:

- knife
- fork
- spoon
- glass
- cup
- plate

## Dataset Description

Initailly the dataset was taken from the Kaggle competition which can be found [here](https://www.kaggle.com/competitions/kitchenware-classification). Then it was processed to create labels for test data and then it was split into `train`, `test`, and `eval-images` directories. The notebooks to generate cleaned data are kept in the [data-generator](data-generator) directory.

The `train` and `test` directories have the sub-directories which belong to 6 classes, whereas `eval-images` directory only contains the 6 images representing each class to test model performance on the unseen examples.


## Project File Structure and Data

The file structure for the project looks like this:

```
.
|-- LICENSE
|-- README.md
|-- assets
|   |-- bg-image.jpg
|   |-- demo.mp4
|   |-- ...
|-- data-generator
|   |-- kitchenware-datagenerator-part1.ipynb
|   `-- kitchenware-datagenerator-part2.ipynb
|-- datasets
|   |-- kitchenware-dataset
|   |   |-- eval-images
|   |   |   |-- 0196.jpg
|   |   |   |-- 0820.jpg
|   |   |   |-- 1956.jpg
|   |   |   |-- 4470.jpg
|   |   |   |-- 4567.jpg
|   |   |   `-- 5768.jpg
|   |   |-- test
|   |   |   |-- cup
|   |   |   |   |-- 0000.jpg
|   |   |   |   |-- 0008.jpg
|   |   |   |   |-- 0011.jpg
|   |   |   |   |-- ...
|   |   |   |-- fork
|   |   |   |   |-- 0076.jpg
|   |   |   |   |-- 0096.jpg
|   |   |   |   |-- 0121.jpg
|   |   |   |   |-- ...
|   |   |   |-- glass
|   |   |   |   |-- 0022.jpg
|   |   |   |   |-- 0042.jpg
|   |   |   |   |-- 0055.jpg
|   |   |   |   |-- ...
|   |   |   |-- knife
|   |   |   |   |-- 0018.jpg
|   |   |   |   |-- 0034.jpg
|   |   |   |   |-- 0059.jpg
|   |   |   |   |-- ...
|   |   |   |-- plate
|   |   |   |   |-- 0002.jpg
|   |   |   |   |-- 0007.jpg
|   |   |   |   |-- 0019.jpg
|   |   |   |   |-- ...
|   |   |   `-- spoon
|   |   |       |-- 0001.jpg
|   |   |       |-- 0024.jpg
|   |   |       |-- 0033.jpg
|   |   |       |-- ...
|   |   `-- train
|   |       |-- cup
|   |       |   |-- 0003.jpg
|   |       |   |-- 0006.jpg
|   |       |   |-- 0009.jpg
|   |       |   |-- ...
|   |       |-- fork
|   |       |   |-- 0036.jpg
|   |       |   |-- 0063.jpg
|   |       |   |-- 0106.jpg
|   |       |   |-- ...
|   |       |-- glass
|   |       |   |-- 0021.jpg
|   |       |   |-- 0039.jpg
|   |       |   |-- 0045.jpg
|   |       |   |-- ...
|   |       |-- knife
|   |       |   |-- 0012.jpg
|   |       |   |-- 0013.jpg
|   |       |   |-- 0016.jpg
|   |       |   |-- ...
|   |       |-- plate
|   |       |   |-- 0004.jpg
|   |       |   |-- 0010.jpg
|   |       |   |-- 0014.jpg
|   |       |   |-- ...
|   |       `-- spoon
|   |           |-- 0005.jpg
|   |           |-- 0032.jpg
|   |           |-- 0040.jpg
|   |           |-- ...
|   `-- kitchenware-dataset.zip
|-- deployment
|   |-- Dockerfile
|   |-- Pipfile
|   |-- Pipfile.lock
|   |-- img_preprocessor.py
|   |-- kitchenware-model.tflite
|   |-- lambda_function.py
|   |-- requirements.txt
|   |-- stream.py
|   `-- test.py
|-- models
|   |-- efficientnetb0_14_0.962.h5
|   `-- kitchenware-model.tflite
|-- notebooks
|   |-- 01-model-training.ipynb
|   |-- 02-model-evaluation.ipynb
|   `-- 03-tflite-model.ipynb
|-- requirements.txt
`-- tflite-runtime-binaries
    |-- tflite_runtime-2.5.0.post1-cp39-cp39-linux_x86_64.whl
    |-- tflite_runtime-2.5.0.post1-cp39-cp39-macosx_11_0_x86_64.whl
    `-- tflite_runtime-2.5.0.post1-cp39-cp39-win_amd64.whl
```

The structure description:

- `assets`: directory to store video and images
- `data-generator`: directory contains data generator notebooks; `kitchenware-datagenerator-part1.ipynb` to create labels for test data and `kitchenware-datagenerator-part2.ipynb` to split data into train (85%), test (15%), and evaluation images to test model performance.
- `datasets`: directory contains datasets
- `deployment`: directory contains all the relevant files for model deployment and web app
- `models`: directory to store models
- `notebooks`: directory contains notebooks
- `requirements.txt`: file contains name and version of the required packages to work with the project
- `tflite-runtime-binaries`: directory contains tflite runtime binaries for Windows, Linux, and MacOS (more on this later)

> Note: The cleaned dataset is provided therefore, notebooks in `data-generator` are not required to use. But if you wish to use them in that case you'll have to download the dataset from the original source including `csv` files. The link is given above.

## Initial Setup and Download Data

