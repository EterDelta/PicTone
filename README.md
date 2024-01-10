# PicTone


![Language](https://img.shields.io/badge/language-Python%203.6-3572A5.svg?style=flat-square)
![GitHub license](https://img.shields.io/github/license/EterDelta/PicTone?style=flat-square)

PicTone is a simple, fun Python CLI tool that converts images into vectorscope audios. It supports tweaking multiple parameters and sampling sequences of images.

## Installation
To install PicTone, use pip:
```bash
pip install pictone
```
You'll need Python 3.6 or higher.

## Usage
PicTone is a command-line tool that converts the images into WAV files using a sampler with edge detection.
You can tweak its parameters and the way the images are passed to it.

### Command Line
The basic command structure for using PicTone is as follows:
```bash
pictone -i input_path -o output_path [options]
```
Input can be either an image or a folder with an ordered sequence of them.

In addition to the required input and output paths, there are some optional arguments to shape the result:

- `-r` `--rate`: Sample rate for the output audio. Default is 44100 Hz.
- `-d` `--depth`: Bit depth for audio samples. Can be 8, 16, or 24. Default is 16.
- `-s` `--samples`: Number of samples the inputs should be forced to last. By default, they'll last the minimum. This is useful if you are converting a sequence (e.g. Forcing to 735 with a rate of 44100 would achieve a ~60 fps visualization).
- `-a` `--aspect`: Boolean value to decide whether to preserve the input aspect ratio. Defaults to `True`.

### As a Library
If you want to experiment, the sampler can be instantiated and configured by yourself. Although it just outputs a single input raw data:
```python
import cv2
from pictone.sampler import EdgeSampler

image = cv2.imread("image.png", 0)
image_edges = cv2.Canny(image, 100, 200)

edge_threshold = 0
byte_depth = 2

sampler = EdgeSampler(edge_threshold, byte_depth) # Basic params

sampled_data = sampler.sample_frames(image_edges)
```
