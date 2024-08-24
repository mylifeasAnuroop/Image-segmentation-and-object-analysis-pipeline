
# import sys
# import os
# import streamlit as st
# import json

# # Add the parent directory of 'utils' to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from utils.preprocessing import preprocess  # Updated import
# from models.segmentation_model import run_segmentation
# from models.identification_model import run_identification
# from models.text_extraction_model import run_text_extraction
# from models.summarization_model import run_summarization
# from utils.data_mapping import map_data
# from utils.visualization import generate_final_metadata

# # Define paths relative to the parent folder of the Streamlit app
# input_images_path = os.path.join('..', 'data', 'input_images')
# segmented_objects_path = os.path.join('..', 'data', 'segmented_objects')
# output_path = os.path.join('..', 'data', 'output')
# metadata_file = os.path.join(output_path, 'metadata.json')
# final_metadata_file = os.path.join(output_path, 'final_metadata.json')

# # Ensure that the input_images directory exists
# if not os.path.exists(input_images_path):
#     os.makedirs(input_images_path)

# # Set up the Streamlit app with a light color theme
# st.set_page_config(page_title="Image Intelligence Hub", layout="wide", initial_sidebar_state="expanded")

# # Inject custom CSS directly into the Streamlit app
# st.markdown("""
#     <style>
#         body {
#             background-color: #f5f5f5; /* Light background color */
#         }

#         .sidebar .sidebar-content {
#             background-color: #ffffff; /* Light sidebar background */
#         }

#         .stButton>button {
#             background-color: #007bff; /* Button color */
#             color: white;
#             border: none;
#         }

#         .stAlert {
#             color: #333333; /* Text color in alerts */
#         }

#         .stMarkdown {
#             color: #333333; /* Text color in markdown */
#         }

#         .stSpinner>div {
#             border-top-color: #007bff; /* Spinner color */
#         }

#         .stImage img {
#             border: 1px solid #cccccc; /* Border around images */
#         }
#     </style>
# """, unsafe_allow_html=True)

# st.title("Image Intelligence Hub")
# st.subheader("AI Pipeline for Image Segmentation and Object Analysis")

# # Sidebar with additional options
# st.sidebar.header("App Options")
# upload_multiple = st.sidebar.checkbox("Enable Multiple Image Uploads")
# progress_bar = st.sidebar.checkbox("Show Progress Indicators", value=True)
# allow_download = st.sidebar.checkbox("Allow Download of Results", value=True)
# add_annotations = st.sidebar.checkbox("Enable Custom Annotations")

# # Upload image(s)
# uploaded_files = st.file_uploader(
#     "Upload Image(s) for Analysis", type=['png', 'jpg', 'jpeg'], accept_multiple_files=upload_multiple)

# if uploaded_files:
#     if not isinstance(uploaded_files, list):
#         uploaded_files = [uploaded_files]

#     for uploaded_file in uploaded_files:
#         # Save uploaded file
#         temp_dir = 'temp'
#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)
#         uploaded_file_path = os.path.join(temp_dir, uploaded_file.name)
#         with open(uploaded_file_path, 'wb') as f:
#             f.write(uploaded_file.getbuffer())

#         # Preprocess to clear old files and move the new image
#         st.info(f"Preparing environment by cleaning old files and moving {uploaded_file.name}...")
#         preprocess(uploaded_file.name)  # Updated function call
#         st.success(f"Image {uploaded_file.name} prepared successfully!")

#         # Step 1: Image Segmentation
#         if progress_bar:
#             with st.spinner("Running segmentation model..."):
#                 run_segmentation(input_images_path, segmented_objects_path)
#         else:
#             st.info("Running segmentation model...")
#             run_segmentation(input_images_path, segmented_objects_path)
#         st.success("Segmentation completed!")

#         # Step 2: Object Identification
#         if progress_bar:
#             with st.spinner("Running identification model..."):
#                 run_identification(segmented_objects_path, metadata_file)
#         else:
#             st.info("Running identification model...")
#             run_identification(segmented_objects_path, metadata_file)
#         st.success("Identification completed!")

#         # Step 3: Text Extraction
#         if progress_bar:
#             with st.spinner("Running text extraction model..."):
#                 run_text_extraction()
#         else:
#             st.info("Running text extraction model...")
#             run_text_extraction()
#         st.success("Text extraction completed!")

#         # Step 4: Summarization
#         if progress_bar:
#             with st.spinner("Running summarization model..."):
#                 run_summarization(metadata_file)  # Pass the metadata file path here
#         else:
#             st.info("Running summarization model...")
#             run_summarization(metadata_file)  # Pass the metadata file path here
#         st.success("Summarization completed!")

#         # Step 5: Data Mapping
#         if progress_bar:
#             with st.spinner("Mapping data..."):
#                 map_data()
#         else:
#             st.info("Mapping data...")
#             map_data()
#         st.success("Data mapping completed!")

#         # Step 6: Visualization
#         if progress_bar:
#             with st.spinner("Generating final metadata and visualization..."):
#                 final_metadata = generate_final_metadata()
#         else:
#             st.info("Generating final metadata and visualization...")
#             final_metadata = generate_final_metadata()
#         st.success("Visualization ready!")

#         # Display final output
#         st.header("Analysis Results")

#         # Load final metadata
#         if os.path.exists(final_metadata_file):
#             with open(final_metadata_file, 'r') as f:
#                 final_metadata = json.load(f)

#             for image_name, metadata in final_metadata.items():
#                 # Determine the master image path
#                 master_image_name = 'annotated_' + uploaded_file.name
#                 master_image_path = os.path.join(output_path, master_image_name)

#                 # Display master image
#                 if os.path.exists(master_image_path):
#                     st.subheader("Master Image")
#                     st.image(master_image_path, caption="Master Image")
#                 else:
#                     st.error(f"Master image not found: {master_image_path}")

#                 # Display segmented objects and summaries
#                 for obj in metadata['segmented_objects']:
#                     st.subheader(f"Segmented Object")

#                     object_image_path = os.path.join(segmented_objects_path, os.path.basename(obj['object_image']))
#                     if os.path.exists(object_image_path):
#                         st.image(object_image_path, caption="Segmented Object")
#                     else:
#                         st.error(f"Segmented object image not found: {object_image_path}")

#                     summary_table_path = os.path.join(output_path, os.path.basename(obj['summary_table']))
#                     if os.path.exists(summary_table_path):
#                         st.image(summary_table_path, caption="Summary Table")
#                     else:
#                         st.error(f"Summary table not found: {summary_table_path}")

#                     # Custom Annotations
#                     if add_annotations:
#                         annotation = st.text_input(f"Add annotation for {obj['object_image']}:", key=f"annotation_{obj['object_image']}")
#                         if st.button(f"Save Annotation for {obj['object_image']}", key=f"save_annotation_{obj['object_image']}"):
#                             # Code to save the annotation (e.g., updating the metadata or saving to a file)
#                             st.success(f"Annotation saved for {obj['object_image']}!")

#         else:
#             st.error("No final metadata available. Please ensure all steps are completed.")

#         # Download final metadata
#         if allow_download:
#             st.write(f"Final Metadata saved to: {final_metadata_file}")
#             st.download_button(
#                 "Download Final Metadata", json.dumps(final_metadata), "final_metadata.json", "application/json"
#             )



import sys
import os
import streamlit as st
import json

# Add the parent directory of 'utils' to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.preprocessing import preprocess
from models.segmentation_model import run_segmentation
from models.identification_model import run_identification
from models.text_extraction_model import run_text_extraction
from models.summarization_model import run_summarization
from utils.data_mapping import map_data
from utils.visualization import generate_final_metadata

# Define paths relative to the parent folder of the Streamlit app
input_images_path = os.path.join('..', 'data', 'input_images')
segmented_objects_path = os.path.join('..', 'data', 'segmented_objects')
output_path = os.path.join('..', 'data', 'output')
metadata_file = os.path.join(output_path, 'metadata.json')
final_metadata_file = os.path.join(output_path, 'final_metadata.json')

# Ensure that the input_images directory exists
if not os.path.exists(input_images_path):
    os.makedirs(input_images_path)

# Set up the Streamlit app with a light color theme
st.set_page_config(page_title="Image Intelligence Hub", layout="wide", initial_sidebar_state="expanded")

# Inject custom CSS directly into the Streamlit app
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5; /* Light background color */
        }

        .sidebar .sidebar-content {
            background-color: #ffffff; /* Light sidebar background */
        }

        .stButton>button {
            background-color: #007bff; /* Button color */
            color: white;
            border: none;
        }

        .stAlert {
            color: #333333; /* Text color in alerts */
        }

        .stMarkdown {
            color: #333333; /* Text color in markdown */
        }

        .stSpinner>div {
            border-top-color: #007bff; /* Spinner color */
        }

        .stImage img {
            border: 1px solid #cccccc; /* Border around images */
        }
    </style>
""", unsafe_allow_html=True)

st.title("Image Intelligence Hub")
st.subheader("AI Pipeline for Image Segmentation and Object Analysis")

# Sidebar with additional options
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
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        uploaded_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(uploaded_file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Preprocess to clear old files and move the new image
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

        # Step 6: Visualization
        if progress_bar:
            with st.spinner("Generating final metadata and visualization..."):
                generate_final_metadata()
        else:
            st.info("Generating final metadata and visualization...")
            generate_final_metadata()
        st.success("Visualization ready!")

        # Display final output
        st.header("Analysis Results")

        # Load final metadata
        final_metadata = {}
        if os.path.exists(final_metadata_file):
            st.info(f"Final metadata file found at: {final_metadata_file}")
            try:
                with open(final_metadata_file, 'r') as f:
                    final_metadata = json.load(f)
            except json.JSONDecodeError as e:
                st.error(f"Error loading JSON data: {e}")

            if not final_metadata:
                st.error("Final metadata is empty. Please check the file content.")
        else:
            st.error("No final metadata available. Please ensure all steps are completed.")

        if final_metadata:
            for image_name, metadata in final_metadata.items():
                st.subheader(f"Results for {image_name}")

                # Display master image
                master_image_path = metadata.get('master_image')
                if master_image_path and os.path.exists(master_image_path):
                    st.image(master_image_path, caption="Master Image", use_column_width=True)
                else:
                    st.error(f"Master image not found: {master_image_path}")

                # Display segmented objects and their summary tables
                for obj in metadata.get('segmented_objects', []):
                    st.subheader("Segmented Object")

                    object_image_path = obj.get('object_image')
                    summary_table_path = obj.get('summary_table')

                    if object_image_path and os.path.exists(object_image_path):
                        st.image(object_image_path, caption="Segmented Object", use_column_width=True)
                    else:
                        st.error(f"Segmented object image not found: {object_image_path}")

                    if summary_table_path and os.path.exists(summary_table_path):
                        st.image(summary_table_path, caption="Summary Table", use_column_width=True)
                    else:
                        st.error(f"Summary table not found: {summary_table_path}")

                    # Custom Annotations
                    if add_annotations:
                        annotation = st.text_input(f"Add annotation for {obj.get('object_image', '')}:", key=f"annotation_{obj.get('object_image', '')}")
                        if st.button(f"Save Annotation for {obj.get('object_image', '')}", key=f"save_annotation_{obj.get('object_image', '')}"):
                            # Code to save the annotation (e.g., updating the metadata or saving to a file)
                            st.success(f"Annotation saved for {obj.get('object_image', '')}!")

        # Download final metadata
        if allow_download:
            st.write(f"Final Metadata saved to: {final_metadata_file}")
            try:
                # Ensure final_metadata is not empty and is serializable
                if final_metadata:
                    st.download_button(
                        "Download Final Metadata", json.dumps(final_metadata), "final_metadata.json", "application/json"
                    )
                else:
                    st.warning("No metadata available for download.")
            except Exception as e:
                st.error(f"Error creating download button: {e}")
