# AI Pipeline for Image Segmentation and Object Analysis 
Switch to Master branch 
#### Author : Anuroop Arya

## Overview

This project entails developing an AI pipeline for image segmentation and object analysis. The pipeline examines an input image to segment, identify, and analyze items within it, and then generates a summary table with mapping data for each one. The project covers activities such as segmentation, object extraction, identification, text/data extraction, summarization, data mapping, and output production, as well as a Streamlit user interface for pipeline testing..

## Features

- **Image Segmentation**: Uses a pre-trained Mask R-CNN model for precise object segmentation.
- **Object Identification**: Leverages the CLIP model for accurate identification and description of objects.
- **Text Extraction**: Extracts text from object images using EasyOCR, ideal for identifying embedded textual data.
- **Summarization**: Utilizes NLP models to summarize text and attributes associated with each object.
- **Metadata Management**: Stores and manages object data using JSON for easy retrieval and analysis.

## Requirements

The required Python packages are listed in the `requirements.txt` file:

```
altair==5.4.0
attrs==24.2.0
blinker==1.8.2
cachetools==5.5.0
certifi==2024.7.4
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
contourpy==1.2.1
cycler==0.12.1
easyocr==1.7.1
filelock==3.15.4
fonttools==4.53.1
fsspec==2024.6.1
gitdb==4.0.11
GitPython==3.1.43
huggingface-hub==0.24.6
idna==3.8
imageio==2.35.1
Jinja2==3.1.4
jsonschema==4.23.0
jsonschema-specifications==2023.12.1
kiwisolver==1.4.5
lazy_loader==0.4
markdown-it-py==3.0.0
MarkupSafe==2.1.5
matplotlib==3.9.2
mdurl==0.1.2
mpmath==1.3.0
narwhals==1.5.4
networkx==3.3
ninja==1.11.1.1
numpy==1.26.4
opencv-python==4.10.0.84
opencv-python-headless==4.10.0.84
packaging==24.1
pandas==2.2.2
pillow==10.4.0
protobuf==5.27.3
pyarrow==17.0.0
pyclipper==1.3.0.post5
pydeck==0.9.1
Pygments==2.18.0
pyparsing==3.1.2
python-bidi==0.6.0
python-dateutil==2.9.0.post0
pytz==2024.1
PyYAML==6.0.2
referencing==0.35.1
regex==2024.7.24
requests==2.32.3
rich==13.7.1
rpds-py==0.20.0
safetensors==0.4.4
scikit-image==0.24.0
scipy==1.14.1
setuptools==73.0.1
shapely==2.0.6
six==1.16.0
smmap==5.0.1
streamlit==1.37.1
sympy==1.13.2
tenacity==8.5.0
tifffile==2024.8.10
tokenizers==0.19.1
toml==0.10.2
torch==2.4.0
torchvision==0.19.0
tornado==6.4.1
tqdm==4.66.5
transformers==4.44.2
typing_extensions==4.12.2
tzdata==2024.1
urllib3==2.2.2
watchdog==4.0.2
```

Install the required packages using:

```bash
pip install -r requirements.txt
```

## Pipeline Workflow

1. **Image Upload**: The user uploads an image via the Streamlit UI, which is stored in the `data/input_images` directory.
2. **Preprocessing**: The image is preprocessed using the `preprocessing.py` script integrated with the segmentation model.
3. **Segmentation**: The image is segmented into objects, each assigned a unique ID. The segmented images are saved in the `data/segmented_objects` directory.
4. **Identification**: Segmented objects are identified using the identification model, and the results are saved as `metadata.json` in the `data/output` directory.
5. **Text Extraction**: Text, if present, is extracted from the segmented images and added to the `metadata.json` file.
6. **Summarization**: Summaries of extracted text are generated and appended to the metadata file.
7. **Data Mapping**: The data is mapped, and a final JSON file (`final_mapping.json`) is created, containing links to the images and corresponding metadata.
8. **Visualization**: The `visualization.py` script prepares the final output and generates a summary table in `final_metadata.json`, ready for display in the Streamlit app.

## Folder Structure


```
Segmentation_project/
│
├── data/
│   ├── input_images/               # Directory for input images
│   ├── segmented_objects/          # Directory to save segmented object images
│   └── output/                     # Directory for output images and tables
│
├── models/
│   ├── segmentation_model.py       # Script for segmentation model
│   ├── identification_model.py     # Script for object identification model
│   ├── text_extraction_model.py    # Script for text/data extraction model
│   └── summarization_model.py      # Script for summarization model
│
├── utils/
│   ├── preprocessing.py            # Script for preprocessing functions
│   ├── data_mapping.py             # Script for data mapping functions
│   └── visualization.py            # Script for visualization functions
│
├── tests/
│   ├── test_segmentation.py        # Tests for segmentation
│   ├── test_identification.py      # Tests for identification
│   ├── test_text_extraction.py     # Tests for text extraction
│   ├── test_summarization.py       # Tests for summarization
│
├── README.md                       # Project overview and setup instructions
├── requirements.txt                # Required Python packages
├── presentation.pptx               # Presentation slides summarizing the project
└── app.py                          # Streamlit app for pipeline testing
```
`

## Example Output

### Original Input Image
![Original Input Image](https://github.com/mylifeasAnuroop/anuroop-arya-wasserstoff-AiInternTask/blob/master/Segmentation_project/data/input_images/hooman.jpg)

### Segmented Image
![Segmented Object Image](https://github.com/mylifeasAnuroop/anuroop-arya-wasserstoff-AiInternTask/blob/master/Segmentation_project/data/segmented_objects/hooman_object_0.png)

## Known Limitations

- The pipeline may need adjustments for handling images with complex backgrounds or overlapping objects.
- Text extraction accuracy can vary depending on the quality and font of the text in the images.

### Contact

For more information, feel free to reach out:

- Email: goodanuroop@gmail.com
- LinkedIn: [Anuroop Arya](https://www.linkedin.com/in/anuroop-arya-803b2625b/)




