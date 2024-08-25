
import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Correct PROJECT_ROOT to point to the Segmentation_project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the correct paths to various directories and files within the project
FINAL_MAPPING_FILE = os.path.join(PROJECT_ROOT, 'data', 'output', 'final_mapping.json')
SEGMENTED_IMAGES_DIR = os.path.join(PROJECT_ROOT, 'data', 'segmented_objects')
INPUT_IMAGES_DIR = os.path.join(PROJECT_ROOT, 'data', 'input_images')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'output')

print("Script started.")  # Indicate that the script execution has started

# Function to load the final_mapping.json file and return its content as a Python dictionary
def load_final_mapping(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Debugging information: print paths and file listings for the relevant directories
print(f"Input Images Directory: {INPUT_IMAGES_DIR}")
print(f"Files in Input Images Directory: {os.listdir(INPUT_IMAGES_DIR)}")

print(f"Segmented Images Directory: {SEGMENTED_IMAGES_DIR}")
print(f"Files in Segmented Images Directory: {os.listdir(SEGMENTED_IMAGES_DIR)}")

print(f"Final Mapping File: {FINAL_MAPPING_FILE}")
try:
    # Attempt to load the final mapping JSON file and print its content
    final_mapping = load_final_mapping(FINAL_MAPPING_FILE)
    print(f"Final Mapping Loaded: {final_mapping}")
except Exception as e:
    # Print an error message if the file cannot be loaded
    print(f"Error loading final mapping: {e}")

# Function to draw bounding boxes on the given axes with the specified label and color
def draw_bbox(ax, bbox, label, color='red'):
    x1, y1, x2, y2 = bbox  # Extract the coordinates from the bounding box
    width = x2 - x1  # Calculate the width of the bounding box
    height = y2 - y1  # Calculate the height of the bounding box
    rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor=color, facecolor='none')
    ax.add_patch(rect)  # Add the rectangle patch to the axes
    ax.text(x1, y1 - 5, label, color=color, fontsize=10, weight='bold')  # Add the label above the bounding box

# Function to plot an image with annotations and save the result to the output directory
def plot_image_with_annotations(master_image_path, output_dir):
    if not os.path.exists(master_image_path):
        # Warn the user if the specified image file is not found
        print(f"Warning: Image file {master_image_path} not found.")
        return

    # Open the image using PIL and create a Matplotlib figure with axes
    image = Image.open(master_image_path)
    fig, ax = plt.subplots(1)
    ax.imshow(image)  # Display the image on the axes

    # Define the bounding box for the entire image and draw it
    bbox = [0, 0, image.width, image.height]
    draw_bbox(ax, bbox, 'Master Image', color='blue')

    # Save the annotated image to the output directory
    output_image_path = os.path.join(output_dir, f'annotated_{os.path.basename(master_image_path)}')
    plt.axis('off')  # Remove axis ticks and labels
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)  # Save the figure
    plt.close(fig)  # Close the figure to free memory
    
    return output_image_path  # Return the path to the saved annotated image

# Function to generate a summary table as an image and save it to the output directory
def generate_summary_table(object_name, master_image_data, output_dir):
    # Prepare the table data using details from the master_image_data dictionary
    table_data = [
        [
            master_image_data.get('detection', {}).get('description', ''),
            f"{master_image_data.get('detection', {}).get('probability', 0):.2f}",
            master_image_data.get('texts', ''),
            master_image_data.get('summary', '')
        ]
    ]
    
    # Create a Matplotlib figure and add the table
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.axis('tight')  # Remove extra space around the table
    ax.axis('off')  # Hide the axes

    # Create the table with specified column labels and add it to the axes
    table = ax.table(
        cellText=table_data,
        colLabels=['Description', 'Probability', 'Texts', 'Summary'],
        cellLoc='center',
        loc='center'
    )
    
    # Customize the table's appearance
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.5, 1.5)
    
    # Save the summary table image to the output directory
    output_image_path = os.path.join(output_dir, f'{object_name}_summary_table.jpg')
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0.1, dpi=300)  # Save the figure
    plt.close(fig)  # Close the figure to free memory
    
    return output_image_path  # Return the path to the saved summary table image

# Function to generate the final metadata based on the input images and the final mapping
def generate_final_metadata():
    final_mapping = load_final_mapping(FINAL_MAPPING_FILE)  # Reload the final mapping
    final_metadata = {}  # Initialize an empty dictionary to store the metadata
    
    for image_name in os.listdir(INPUT_IMAGES_DIR):
        image_path = os.path.join(INPUT_IMAGES_DIR, image_name)
        print(f"Processing master image: {image_name}")  # Log the current image being processed

        # Check if the file is an image and not a system file like 'desktop.ini'
        if image_name.lower().endswith(('.jpg', '.jpeg', '.png')) and image_name.lower() != 'desktop.ini':
            # Annotate the master image and get the path to the annotated image
            annotated_image_path = plot_image_with_annotations(image_path, OUTPUT_DIR)

            # Initialize the metadata for the current image
            final_metadata[image_name] = {
                "master_image": os.path.relpath(annotated_image_path, PROJECT_ROOT),
                "segmented_objects": []
            }

            # Loop through each object in the final mapping and generate corresponding summary tables
            for object_name, master_image_data in final_mapping.items():
                segmented_object_path = os.path.join(SEGMENTED_IMAGES_DIR, object_name)
                
                # Check if the segmented image exists for the object
                if object_name in os.listdir(SEGMENTED_IMAGES_DIR):
                    # Generate the summary table and get the path to the saved table image
                    summary_table_path = generate_summary_table(object_name, master_image_data, OUTPUT_DIR)
                    
                    # Add the segmented object and its summary table to the metadata
                    final_metadata[image_name]["segmented_objects"].append({
                        "object_image": os.path.relpath(segmented_object_path, PROJECT_ROOT),
                        "summary_table": os.path.relpath(summary_table_path, PROJECT_ROOT)
                    })
                else:
                    # Log a warning if the segmented image is not found
                    print(f"No corresponding segmented image found for {object_name} in {SEGMENTED_IMAGES_DIR}.")

    # Save the final metadata to a JSON file in the output directory
    final_metadata_file = os.path.join(OUTPUT_DIR, 'final_metadata.json')
    with open(final_metadata_file, 'w') as outfile:
        json.dump(final_metadata, outfile, indent=4)
    print(f"Final metadata saved to {final_metadata_file}")  # Log the successful saving of metadata

    return final_metadata  # Return the generated metadata

generate_final_metadata()  # Execute the function to generate the final metadata

