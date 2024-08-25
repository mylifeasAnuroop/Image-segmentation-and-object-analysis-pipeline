

import os
import shutil

def clear_directory(directory_path, file_types=None, keep_file=None):
    """
    Remove all contents from the specified directory based on file types,
    optionally keeping a specific file.
    
    Parameters:
    directory_path (str): The path to the directory to be cleared.
    file_types (list): List of file extensions to delete (e.g., ['.json', '.jpeg', '.png']).
    keep_file (str): Filename to keep in the directory.
    """
    if os.path.exists(directory_path):
        print(f"Clearing directory: {directory_path}")
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if filename == keep_file:
                continue
            try:
                if file_types:
                    if any(filename.endswith(file_type) for file_type in file_types):
                        print(f"Removing file: {file_path}")
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                else:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        print(f"Removing file: {file_path}")
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        print(f"Removing directory: {file_path}")
                        shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The directory {directory_path} does not exist.")

def preprocess(new_image_name):
    """
    Clear specified directories, keeping only the latest uploaded image, and clean up specific files.
    
    Parameters:
    new_image_name (str): The name of the new input image.
    """
    # Define paths relative to the project root
    script_dir = os.path.dirname(__file__)
    input_images_path = os.path.join(script_dir, '..', 'data', 'input_images')
    segmented_objects_path = os.path.join(script_dir, '..', 'data', 'segmented_objects')
    output_path = os.path.join(script_dir, '..', 'data', 'output')
    temp_dir = os.path.join(script_dir, '..', 'temp')

    # Ensure directories exist
    for path in [input_images_path, segmented_objects_path, output_path, temp_dir]:
        os.makedirs(path, exist_ok=True)

    # Clear the segmented_objects directory (removing .json and image files)
    clear_directory(segmented_objects_path, file_types=['.json', '.jpeg', '.jpg', '.png'])

    # Clear the output directory (removing .json and image files)
    clear_directory(output_path, file_types=['.json', '.jpeg', '.jpg', '.png'])

    # Clear the input_images directory, keeping only the new image
    if os.path.exists(input_images_path):
        for filename in os.listdir(input_images_path):
            file_path = os.path.join(input_images_path, filename)
            if filename != new_image_name:
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        print(f"Removing file: {file_path}")
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        print(f"Removing directory: {file_path}")
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The directory {input_images_path} does not exist.")

    # Move the new input image to the input_images directory
    new_image_path = os.path.join(temp_dir, new_image_name)
    if os.path.exists(new_image_path):
        print(f"Moving new image to {input_images_path}")
        shutil.copy(new_image_path, input_images_path)
    else:
        print(f"The new image {new_image_path} does not exist.")

if __name__ == "__main__":
    # Example usage
    new_image_name = 'new_image.jpg'  # Update with the name of the new image
    preprocess(new_image_name)
