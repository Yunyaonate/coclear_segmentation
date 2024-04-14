# Coclear_Segmentation
<br>

__Aim:__ Semantic Segmentation for cochlear implant from CBCT scans

__Data:__ De-identified CBCT scans of 66 patients, each folder cotains ~1000 DICOM files.

__Solution plan:__ 
1. Learn and load the data (completed)
2. Filter the interested data out. (completed)
3. Label Annotation (partially completed)
4. Preprocessing (completed)
5. Model training (now)
6. Fintune and standardise the model

 # Phrase 1: Learn and load the data
 ## Image inspection
- load 1 DICOM, print the info, and see what can we do with it
- From this section, we know the tags they set, and we are interested in 
    - patient ID
    - ImageOrientationPatient
    - image dimensions
    - PixelData
![image1](img/data_info.jpg)

## Filter: select all coronal images
To create a function that processes all DICOM images in a given folder, checks their `ImageOrientationPatient` attribute, rounds its values to one decimal place, and duplicates the image to a specified folder if the orientation matches `(1,0,0,0,0,-1)`, we use the `pydicom` library for reading DICOM files and the `shutil` library for copying files.

Here is a step-by-step approach to write this function:

1. **Iterate Over All DICOM Files**: Read each DICOM file in the specified folder.

2. **Check `ImageOrientationPatient`**: Extract this attribute from each DICOM file, round the values to one decimal place, and check if it matches the specified orientation.

3. **Copy Matching Files**: If an image matches the criteria, duplicate it to the specified target folder.

---
__After those steps, we get 1700 images that show the coronal plane, where around 38 of them have clear electrode arrays. Now we start with the 38 images__
---

# Phrase 2: Label Annotation
This step is to manually create the true masks for assisting model training. After this phrase, we are supposed to have PNG files that share the same filenames and the same size as the original images, where the pixels for the background are "0" and the pixels for the electrode array are "1". I used 2 methods: 
  1) Use `labelme` to generate masks in JSON format and then convert them into true masks.
  2) Directly use Python to write a GUI, that applies a threshold to filter out most unwanted whiteness, and then use black and pens to modify the mask, then convert to masks

## Labelme Method
First, we manually mark all the labels in labelme.

![image2](img/labelme.jpg)

We will have JSON files that store the label annotation information. Then we visualise and convert them to true masks. See working space:
- [Visualise true mask](https://github.com/Yunyaonate/coclear_segmentation/blob/main/Visualise_true_mask.ipynb), that visualise the mask we just annotated
- [Labelme mask batch](https://github.com/Yunyaonate/coclear_segmentation/blob/main/labelme_mask_batch.ipynb), that covert all the JSON files to mask together

## Python-GUI method
Manually marking every single electrode is painful and could be inaccurate. Thus we create a GUI that uses a threshold filter to find the light area and allow users to manually edit the filtered images with black and white pens, then convert the images into masks. This method is much more effective than using labelme.

The GUI window shows as below:

![image3](img/gui_overview.jpg)

For details, please see working space:
- [Mask generator](https://github.com/Yunyaonate/coclear_segmentation/blob/main/mask_generator.ipynb), where filters most unwanted parts out, and wait for edition, then convert the edited images to mask
- [label GUI](https://github.com/Yunyaonate/coclear_segmentation/blob/main/label_gui.py), where create the GUI

---
Now we have the 38 images with clear electrode arrays and 38 masks that store the annotation as binary images (0 / 255 for easier visualisation) in PNG format. They are ready for model training
---
