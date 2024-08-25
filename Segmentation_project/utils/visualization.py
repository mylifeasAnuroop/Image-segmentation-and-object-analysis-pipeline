
# import os
# import json
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from PIL import Image

# # Correct PROJECT_ROOT to point to the Segmentation_project root
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # Define the correct paths to various directories and files within the project
# FINAL_MAPPING_FILE = os.path.join(PROJECT_ROOT, 'data', 'output', 'final_mapping.json')
# SEGMENTED_IMAGES_DIR = os.path.join(PROJECT_ROOT, 'data', 'segmented_objects')
# INPUT_IMAGES_DIR = os.path.join(PROJECT_ROOT, 'data', 'input_images')
# OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'output')

# print("Script started.")  # Indicate that the script execution has started

# # Function to load the final_mapping.json file and return its content as a Python dictionary
# def load_final_mapping(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

# # Debugging information: print paths and file listings for the relevant directories
# print(f"Input Images Directory: {INPUT_IMAGES_DIR}")
# print(f"Files in Input Images Directory: {os.listdir(INPUT_IMAGES_DIR)}")

# print(f"Segmented Images Directory: {SEGMENTED_IMAGES_DIR}")
# print(f"Files in Segmented Images Directory: {os.listdir(SEGMENTED_IMAGES_DIR)}")

# print(f"Final Mapping File: {FINAL_MAPPING_FILE}")
# try:
#     # Attempt to load the final mapping JSON file and print its content
#     final_mapping = load_final_mapping(FINAL_MAPPING_FILE)
#     print(f"Final Mapping Loaded: {final_mapping}")
# except Exception as e:
#     # Print an error message if the file cannot be loaded
#     print(f"Error loading final mapping: {e}")

# # Function to draw bounding boxes on the given axes with the specified label and color
# def draw_bbox(ax, bbox, label, color='red'):
#     x1, y1, x2, y2 = bbox  # Extract the coordinates from the bounding box
#     width = x2 - x1  # Calculate the width of the bounding box
#     height = y2 - y1  # Calculate the height of the bounding box
#     rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor=color, facecolor='none')
#     ax.add_patch(rect)  # Add the rectangle patch to the axes
#     ax.text(x1, y1 - 5, label, color=color, fontsize=10, weight='bold')  # Add the label above the bounding box

# # Function to plot an image with annotations and save the result to the output directory
# def plot_image_with_annotations(master_image_path, output_dir):
#     if not os.path.exists(master_image_path):
#         # Warn the user if the specified image file is not found
#         print(f"Warning: Image file {master_image_path} not found.")
#         return

#     # Open the image using PIL and create a Matplotlib figure with axes
#     image = Image.open(master_image_path)
#     fig, ax = plt.subplots(1)
#     ax.imshow(image)  # Display the image on the axes

#     # Define the bounding box for the entire image and draw it
#     bbox = [0, 0, image.width, image.height]
#     draw_bbox(ax, bbox, 'Master Image', color='blue')

#     # Save the annotated image to the output directory
#     output_image_path = os.path.join(output_dir, f'annotated_{os.path.basename(master_image_path)}')
#     plt.axis('off')  # Remove axis ticks and labels
#     plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)  # Save the figure
#     plt.close(fig)  # Close the figure to free memory
    
#     return output_image_path  # Return the path to the saved annotated image

# # Function to generate a summary table as an image and save it to the output directory
# def generate_summary_table(object_name, master_image_data, output_dir):
#     # Prepare the table data using details from the master_image_data dictionary
#     table_data = [
#         [
#             master_image_data.get('detection', {}).get('description', ''),
#             f"{master_image_data.get('detection', {}).get('probability', 0):.2f}",
#             master_image_data.get('texts', ''),
#             master_image_data.get('summary', '')
#         ]
#     ]
    
#     # Create a Matplotlib figure and add the table
#     fig, ax = plt.subplots(figsize=(12, 3))
#     ax.axis('tight')  # Remove extra space around the table
#     ax.axis('off')  # Hide the axes

#     # Create the table with specified column labels and add it to the axes
#     table = ax.table(
#         cellText=table_data,
#         colLabels=['Description', 'Probability', 'Texts', 'Summary'],
#         cellLoc='center',
#         loc='center'
#     )
    
#     # Customize the table's appearance
#     table.auto_set_font_size(False)
#     table.set_fontsize(12)
#     table.scale(1.5, 1.5)
    
#     # Save the summary table image to the output directory
#     output_image_path = os.path.join(output_dir, f'{object_name}_summary_table.jpg')
#     plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0.1, dpi=300)  # Save the figure
#     plt.close(fig)  # Close the figure to free memory
    
#     return output_image_path  # Return the path to the saved summary table image

# # Function to generate the final metadata based on the input images and the final mapping
# def generate_final_metadata():
#     final_mapping = load_final_mapping(FINAL_MAPPING_FILE)  # Reload the final mapping
#     final_metadata = {}  # Initialize an empty dictionary to store the metadata
    
#     for image_name in os.listdir(INPUT_IMAGES_DIR):
#         image_path = os.path.join(INPUT_IMAGES_DIR, image_name)
#         print(f"Processing master image: {image_name}")  # Log the current image being processed

#         # Check if the file is an image and not a system file like 'desktop.ini'
#         if image_name.lower().endswith(('.jpg', '.jpeg', '.png')) and image_name.lower() != 'desktop.ini':
#             # Annotate the master image and get the path to the annotated image
#             annotated_image_path = plot_image_with_annotations(image_path, OUTPUT_DIR)

#             # Initialize the metadata for the current image
#             final_metadata[image_name] = {
#                 "master_image": os.path.relpath(annotated_image_path, PROJECT_ROOT),
#                 "segmented_objects": []
#             }

#             # Loop through each object in the final mapping and generate corresponding summary tables
#             for object_name, master_image_data in final_mapping.items():
#                 segmented_object_path = os.path.join(SEGMENTED_IMAGES_DIR, object_name)
                
#                 # Check if the segmented image exists for the object
#                 if object_name in os.listdir(SEGMENTED_IMAGES_DIR):
#                     # Generate the summary table and get the path to the saved table image
#                     summary_table_path = generate_summary_table(object_name, master_image_data, OUTPUT_DIR)
                    
#                     # Add the segmented object and its summary table to the metadata
#                     final_metadata[image_name]["segmented_objects"].append({
#                         "object_image": os.path.relpath(segmented_object_path, PROJECT_ROOT),
#                         "summary_table": os.path.relpath(summary_table_path, PROJECT_ROOT)
#                     })
#                 else:
#                     # Log a warning if the segmented image is not found
#                     print(f"No corresponding segmented image found for {object_name} in {SEGMENTED_IMAGES_DIR}.")

#     # Save the final metadata to a JSON file in the output directory
#     final_metadata_file = os.path.join(OUTPUT_DIR, 'final_metadata.json')
#     with open(final_metadata_file, 'w') as outfile:
#         json.dump(final_metadata, outfile, indent=4)
#     print(f"Final metadata saved to {final_metadata_file}")  # Log the successful saving of metadata

#     return final_metadata  # Return the generated metadata

# generate_final_metadata()  # Execute the function to generate the final metadata


import sys
import os
import streamlit as st
import json
import shutil

# Add the parent directory of 'utils' to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.preprocessing import preprocess
from models.segmentation_model import run_segmentation
from models.identification_model import run_identification
from models.text_extraction_model import run_text_extraction
from models.summarization_model import run_summarization
from utils.data_mapping import map_data
from utils.visualization import generate_final_metadata

# Define paths relative to the project root
root_dir = os.path.abspath(os.path.dirname(__file__))
input_images_path = os.path.join(root_dir, 'data', 'input_images')
segmented_objects_path = os.path.join(root_dir, 'data', 'segmented_objects')
output_path = os.path.join(root_dir, 'data', 'output')
metadata_file = os.path.join(output_path, 'metadata.json')
final_metadata_file = os.path.join(output_path, 'final_metadata.json')
temp_dir = os.path.join(root_dir, 'temp')

# Ensure that the directories exist
os.makedirs(input_images_path, exist_ok=True)
os.makedirs(segmented_objects_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)

# Streamlit app setup
st.set_page_config(page_title="Image Intelligence Hub", layout="wide", initial_sidebar_state="expanded")

st.title("Image Intelligence Hub")
st.subheader("AI Pipeline for Image Segmentation and Object Analysis")

# Sidebar options
st.sidebar.header("App Options")
upload_multiple = st.sidebar.checkbox("Enable Multiple Image Uploads")
progress_bar = st.sidebar.checkbox("Show Progress Indicators", value=True)
allow_download = st.sidebar.checkbox("Allow Download of Results", value=True)
add_annotations = st.sidebar.checkbox("Enable Custom Annotations")

# Upload image(s)
uploaded_files = st.file_uploader(
    "Upload Image(s) for Analysis", type=['png', 'jpg', 'jpeg'], accept_multiple_files=upload_multiple)

if uploaded_files:
    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]

    for uploaded_file in uploaded_files:
        # Save uploaded file
        uploaded_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(uploaded_file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Display the uploaded image in a medium-large size to keep the sidebar visible
        st.image(uploaded_file, caption=f"Uploaded Image: {uploaded_file.name}", width=600)

        # Preprocess and move the new image
        st.info(f"Preparing environment by cleaning old files and moving {uploaded_file.name}...")
        preprocess(uploaded_file.name)
        st.success(f"Image {uploaded_file.name} prepared successfully!")

        # Step 1: Image Segmentation
        if progress_bar:
            with st.spinner("Running segmentation model..."):
                run_segmentation(input_images_path, segmented_objects_path)
        else:
            st.info("Running segmentation model...")
            run_segmentation(input_images_path, segmented_objects_path)
        st.success("Segmentation completed!")

        # Step 2: Object Identification
        if progress_bar:
            with st.spinner("Running identification model..."):
                run_identification(segmented_objects_path, metadata_file)
        else:
            st.info("Running identification model...")
            run_identification(segmented_objects_path, metadata_file)
        st.success("Identification completed!")

        # Step 3: Text Extraction
        if progress_bar:
            with st.spinner("Running text extraction model..."):
                run_text_extraction()
        else:
            st.info("Running text extraction model...")
            run_text_extraction()
        st.success("Text extraction completed!")

        # Step 4: Summarization
        if progress_bar:
            with st.spinner("Running summarization model..."):
                run_summarization(metadata_file)
        else:
            st.info("Running summarization model...")
            run_summarization(metadata_file)
        st.success("Summarization completed!")

        # Step 5: Data Mapping
        if progress_bar:
            with st.spinner("Mapping data..."):
                map_data()
        else:
            st.info("Mapping data...")
            map_data()
        st.success("Data mapping completed!")

        # Display final output
        st.header("Analysis Results")

        if os.path.exists(final_metadata_file):
            st.write("Final metadata file found.")
            with open(final_metadata_file, 'r') as f:
                final_metadata = json.load(f)

            # Display the uploaded image again before showing the segments and tables
            st.image(uploaded_file, caption=f"Original Image: {uploaded_file.name}", width=600)

            for image_name, metadata in final_metadata.items():
                for obj in metadata['segmented_objects']:
                    st.subheader(f"Segmented Object")

                    object_image_path = os.path.join(segmented_objects_path, os.path.basename(obj['object_image']))
                    if os.path.exists(object_image_path):
                        st.image(object_image_path, caption="Segmented Object", width=600)
                    else:
                        st.error(f"Segmented object image not found: {object_image_path}")

                    summary_table_path = os.path.join(output_path, os.path.basename(obj['summary_table']))
                    if os.path.exists(summary_table_path):
                        st.image(summary_table_path, caption="Summary Table", width=600)
                    else:
                        st.error(f"Summary table not found: {summary_table_path}")

                    if add_annotations:
                        annotation = st.text_input(f"Add annotation for {obj['object_image']}:", key=f"annotation_{obj['object_image']}")
                        if st.button(f"Save Annotation for {obj['object_image']}"):
                            st.success(f"Annotation saved for {obj['object_image']}!")

        else:
            st.error("No final metadata available. Please ensure all steps are completed.")

        if allow_download:
            st.write(f"Final Metadata saved to: {final_metadata_file}")
            st.download_button(
                "Download Final Metadata", json.dumps(final_metadata), "final_metadata.json", "application/json"
            )




