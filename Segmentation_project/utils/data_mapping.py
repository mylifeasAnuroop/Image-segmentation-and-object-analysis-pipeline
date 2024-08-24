import json
import os

# Define the project root directory path relative to this script's location
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the paths to the JSON files
METADATA_FILE = os.path.join(PROJECT_ROOT, "data", "output", "metadata.json")  # Path to the metadata JSON file
FINAL_MAPPING_FILE = os.path.join(PROJECT_ROOT, "data", "output", "final_mapping.json")  # Path to the final mapping JSON file

# Define the directory where the master images are stored
MASTER_IMAGE_DIR = os.path.join(PROJECT_ROOT, "data", "input_images", "")  # Path to the directory containing the master images

def load_json_data(file_path):
    """
    Load JSON data from a given file path.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        data (dict): The data loaded from the JSON file.
    """
    print(f"Loading data from {file_path}...")
    with open(file_path, 'r') as file:
        data = json.load(file)
    print(f"Data loaded from {file_path}.")
    return data

def map_data_to_master_image(metadata):
    """
    Map metadata to the corresponding master images.

    Parameters:
        metadata (list): A list of metadata entries, each containing an image ID and related data.

    Returns:
        master_image_mapping (dict): A dictionary mapping image IDs to their associated data.
    """
    master_image_mapping = {}
    print("Mapping data to master images...")
    
    # Iterate over each metadata entry and map it to the corresponding master image
    for entry in metadata:
        image_id = entry['image_id']
        print(f"Processing image_id: {image_id}")
        
        # Initialize a new entry in the mapping if the image ID has not been encountered before
        if image_id not in master_image_mapping:
            master_image_mapping[image_id] = {
                'image_path': os.path.join(MASTER_IMAGE_DIR, image_id),  # Path to the master image
                'detection': entry['detection'],  # Detection data from the metadata
                'texts': entry['texts'],  # Texts extracted from the image
                'summary': entry['summary'],  # Summary of the extracted texts
            }
            print(f"Initialized mapping for image_id: {image_id}")
    
    print("Data mapping completed.")
    return master_image_mapping

def generate_final_mapping():
    """
    Generate the final mapping of metadata to master images and save it to a JSON file.
    """
    # Load the metadata from the JSON file
    metadata = load_json_data(METADATA_FILE)
    
    print("Generating final mapping...")
    # Create the final mapping of metadata to master images
    final_mapping = map_data_to_master_image(metadata)
    
    # Save the final mapping to a JSON file
    with open(FINAL_MAPPING_FILE, 'w') as file:
        json.dump(final_mapping, file, indent=4)
    
    print(f"Final mapping written to {FINAL_MAPPING_FILE}.")

def map_data():
    """
    Wrapper function to initiate the process of generating the final mapping.
    """
    generate_final_mapping()

# If this script is run directly, execute the map_data function
if __name__ == "__main__":
    map_data()



