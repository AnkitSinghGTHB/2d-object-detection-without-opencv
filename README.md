# 2d-object-detection-without-opencv
Segments objects in an image by grouping connected pixels with similar RGB values using a flood-fill algorithm. It filters small objects, identifies the largest as the background, and assigns unique IDs. The results are visualized by overlaying object IDs on an output image, skipping the background.
# Image Object Segmentation and Overlay

This project performs object segmentation in an image based on color similarity. It identifies connected components, assigns unique IDs to each object, and generates an overlay image with object IDs.

## Features

- **Flood-Fill Algorithm**: Groups connected pixels with similar RGB values.
- **Object Filtering**: Removes small objects below a size threshold.
- **Background Identification**: Recognizes and labels the largest object as the background.
- **Overlay Generation**: Outputs an image with object IDs displayed.

## Requirements

- Python 3.7+
- Libraries: `Pillow`, `numpy`

Install dependencies with:
```bash
pip install Pillow numpy
```

## Usage 
 
1. Place your input image in the `input` directory and name it `image1.png` (or modify the `file_path` in the script).
 
2. Run the script:

```bash
python script.py
```
 
3. The output image with overlaid object IDs will be saved to the `output` directory as `overlay_with_numbers.png`.

## Parameters 
 
- **Threshold (`threshold`)** : Adjusts color similarity sensitivity (default: 170).
 
- **Min Object Size (`min_object_size`)** : Filters out small objects (default: 100).

## Example 
![](https://media.licdn.com/dms/image/v2/D562DAQHKNbOyV_UpVA/profile-treasury-image-shrink_800_800/profile-treasury-image-shrink_800_800/0/1735273220202?e=1735880400&v=beta&t=d7IP3GuT14E0D83Y4ABrgFb3-GEQleKlunxJn9p1hWg)

## License 
This project is licensed under the MIT License. See `LICENSE` for details.
