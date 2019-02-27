# `np_obb` calculate oriented bounding boxes in python

## About
`np_obb` is a python package to calculate oriented bounding boxes from:
* mask images (boolean numpy arrays)
* label images (integer numpy arrays labeling connected components)
* point lists

![](./illustration/oriented_boxes_on_label.png)

Author: Volker Hilsenstein based on a [stackoverflow post by 
Mario Klingemann](https://stackoverflow.com/questions/32892932/create-the-oriented-bounding-box-obb-with-python-and-numpy).

## Installation

Install directly from this repo using:
```
pip install git+https://github.com/VolkerH/np_obb.git
```

## Usage

See the examples in [the Jupyter notebook in the `example` folder](./example/Oriented%20Bounding%20Boxes%20Examples.ipynb).