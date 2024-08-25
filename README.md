# AI Pipeline for Image Segmentation and Object Analysis

### Author : Anuroop Arya

## Overview

This project aims to develop a robust AI pipeline for image segmentation and object analysis. The pipeline processes an input image to segment, identify, and analyze objects within the image, ultimately producing a summary table with mapped data for each object. The project includes a Streamlit UI for testing and interacting with the pipeline.

## Features

- **Image Segmentation**: Uses a pre-trained Mask R-CNN model for precise object segmentation.
- **Object Identification**: Leverages the CLIP model for accurate identification and description of objects.
- **Text Extraction**: Extracts text from object images using EasyOCR, ideal for identifying embedded textual data.
- **Summarization**: Utilizes NLP models to summarize text and attributes associated with each object.
- **Metadata Management**: Stores and manages object data using JSON for easy retrieval and analysis.

## Requirements

The required Python packages are listed in the `requirements.txt` file:

```bash
altair==5.4.0
attrs==24.2.0
blinker==1.8.2
...
transformers==4.44.2
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

```plaintext
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
│   ├── postprocessing.py           # Script for postprocessing functions
│   ├── data_mapping.py             # Script for data mapping functions
│   └── visualization.py            # Script for visualization functions
│
├── tests/
│   ├── test_segmentation.py        # Tests for segmentation
│   ├── test_identification.py      # Tests for identification
│   ├── test_text_extraction.py     # Tests for text extraction
│   └── test_summarization.py       # Tests for summarization
│
├── README.md                       # Project overview and setup instructions
├── requirements.txt                # Required Python packages
└── app.py                          # Streamlit application script
```

## Example Output

### Original Input Image
![Original Input Image](https://github.com/mylifeasAnuroop/anuroop-arya-wasserstoff-AiInternTask/blob/master/Segmentation_project/data/input_images/hooman.jpg)

### Segmented Image
![Segmented Object Image](https://github.com/mylifeasAnuroop/anuroop-arya-wasserstoff-AiInternTask/blob/master/Segmentation_project/data/segmented_objects/hooman_object_0.png)

## Known Issues or Limitations

- The pipeline may need adjustments for handling images with complex backgrounds or overlapping objects.
- Text extraction accuracy can vary depending on the quality and font of the text in the images.

## Contact

For any questions or support, please contact:  
[goodanuroop@gmail.com](mailto:goodanuroop@gmail.com)
