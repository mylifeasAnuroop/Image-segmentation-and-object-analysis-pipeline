import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Define directory and file paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FINAL_MAPPING_FILE = os.path.join(PROJECT_ROOT, 'data', 'output', 'final_mapping.json')
SEGMENTED_IMAGES_DIR = os.path.join(PROJECT_ROOT, 'data', 'segmented_objects')
INPUT_IMAGES_DIR = os.path.join(PROJECT_ROOT, 'data', 'input_images')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'output')

def load_final_mapping(file_path):
    """
    Load final mapping data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing the final mapping.
    
    Returns:
        dict: Final mapping data loaded from the JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def draw_bbox(ax, bbox, label, color='red'):
    """
    Draw a bounding box on a matplotlib axis with a label.
    
    Args:
        ax (matplotlib.axes.Axes): The axis to draw on.
        bbox (list): Bounding box coordinates [x1, y1, x2, y2].
        label (str): Label for the bounding box.
        color (str): Color of the bounding box.
    """
    x1, y1, x2, y2 = bbox
    width = x2 - x1
    height = y2 - y1
    rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor=color, facecolor='none')
    ax.add_patch(rect)
    ax.text(x1, y1 - 5, label, color=color, fontsize=10, weight='bold')

def plot_image_with_annotations(master_image_path, output_dir):
    """
    Plot an image with an annotation of its full extent and save the result.
    
    Args:
        master_image_path (str): Path to the master image.
        output_dir (str): Directory where the annotated image will be saved.
    
    Returns:
        str: Path to the saved annotated image.
    """
    if not os.path.exists(master_image_path):
        print(f"Warning: Image file {master_image_path} not found.")
        return

    image = Image.open(master_image_path)
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    # Draw bounding box for the whole image
    bbox = [0, 0, image.width, image.height]
    draw_bbox(ax, bbox, 'Master Image', color='blue')

    output_image_path = os.path.join(output_dir, f'annotated_{os.path.basename(master_image_path)}')
    plt.axis('off')
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    
    return output_image_path

def generate_summary_table(object_name, master_image_data, output_dir):
    """
    Generate a summary table for a given object and save it as an image.
    
    Args:
        object_name (str): Name of the object.
        master_image_data (dict): Data related to the master image and object.
        output_dir (str): Directory where the summary table image will be saved.
    
    Returns:
        str: Path to the saved summary table image.
    """
    table_data = [
        [
            master_image_data.get('detection', {}).get('description', ''),
            f"{master_image_data.get('detection', {}).get('probability', 0):.2f}",
            master_image_data.get('texts', ''),
            master_image_data.get('summary', '')
        ]
    ]
    
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.axis('tight')
    ax.axis('off')

    # Enhanced table styling
    table = ax.table(
        cellText=table_data,
        colLabels=['Description', 'Probability', 'Texts', 'Summary'],
        cellLoc='center',
        loc='center',
        cellColours=[['#d0d0d0']*4],
        colColours=['#a0a0a0']*4,
        edges='closed'
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.5, 1.5)
    
    # Customize table aesthetics
    for key, cell in table._cells.items():
        cell.set_edgecolor('black')
        cell.set_linewidth(1)
        if key[0] == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#707070')
        else:
            cell.set_facecolor('#d0d0d0')
    
    output_image_path = os.path.join(output_dir, f'{object_name}_summary_table.jpg')
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close(fig)
    
    return output_image_path

def generate_final_metadata():
    """
    Generate final metadata including annotated images and summary tables for each image.
    
    Returns:
        dict: Final metadata containing paths to master images and segmented objects.
    """
    final_mapping = load_final_mapping(FINAL_MAPPING_FILE)
    final_metadata = {}
    
    for image_name in os.listdir(INPUT_IMAGES_DIR):
        image_path = os.path.join(INPUT_IMAGES_DIR, image_name)

        if image_name.lower().endswith(('.jpg', '.jpeg', '.png')) and image_name.lower() != 'desktop.ini':
            print(f"Processing master image: {image_name}")
            annotated_image_path = plot_image_with_annotations(image_path, OUTPUT_DIR)

            final_metadata[image_name] = {
                "master_image": os.path.relpath(annotated_image_path, PROJECT_ROOT),
                "segmented_objects": []
            }

            for object_name, master_image_data in final_mapping.items():
                segmented_object_path = os.path.join(SEGMENTED_IMAGES_DIR, object_name)
                
                if object_name in os.listdir(SEGMENTED_IMAGES_DIR):
                    summary_table_path = generate_summary_table(object_name, master_image_data, OUTPUT_DIR)
                    
                    final_metadata[image_name]["segmented_objects"].append({
                        "object_image": os.path.relpath(segmented_object_path, PROJECT_ROOT),
                        "summary_table": os.path.relpath(summary_table_path, PROJECT_ROOT)
                    })
                else:
                    print(f"No corresponding segmented image found for {object_name} in {SEGMENTED_IMAGES_DIR}.")

    final_metadata_file = os.path.join(OUTPUT_DIR, 'final_metadata.json')
    with open(final_metadata_file, 'w') as outfile:
        json.dump(final_metadata, outfile, indent=4)
    print(f"Final metadata saved to {final_metadata_file}")

    return final_metadata

