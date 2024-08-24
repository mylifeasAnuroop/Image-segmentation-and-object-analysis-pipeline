from PIL import Image
import torchvision.transforms as T
import torchvision.models as models
from torchvision.models.detection import MaskRCNN_ResNet50_FPN_Weights
import torch
import numpy as np
import os
import sys

# Define the transformation to convert images to tensors
transform = T.Compose([T.ToTensor()])

# Load the Mask R-CNN model with COCO weights for object detection and segmentation
model = models.detection.maskrcnn_resnet50_fpn(weights=MaskRCNN_ResNet50_FPN_Weights.COCO_V1)
model.eval()  # Set the model to evaluation mode

# Check if a GPU is available and use it if possible; otherwise, use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def resize_image(image, max_size=800):
    """
    Resize the input image to ensure that its width or height does not exceed max_size.
    
    Args:
        image (PIL.Image): The image to resize.
        max_size (int): The maximum width or height of the resized image.
    
    Returns:
        PIL.Image: The resized image.
    """
    width, height = image.size
    if width > max_size or height > max_size:
        if width > height:
            ratio = max_size / float(width)
            new_width = max_size
            new_height = int(height * ratio)
        else:
            ratio = max_size / float(height)
            new_height = max_size
            new_width = int(width * ratio)
        image = image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
    return image

def save_segmented_objects(image, predictions, image_filename, output_dir, threshold=0.5):
    """
    Save segmented objects from the image based on model predictions.
    
    Args:
        image (PIL.Image): The original image.
        predictions (list): The model predictions for the image.
        image_filename (str): The filename of the image.
        output_dir (str): Directory where segmented images will be saved.
        threshold (float): The confidence threshold to filter predictions.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the output directory if it does not exist

    image_np = np.array(image)  # Convert the image to a numpy array

    # Iterate through masks and scores
    for i, (mask, score) in enumerate(zip(predictions[0]['masks'], predictions[0]['scores'])):
        if score > threshold:  # Only save objects with a score above the threshold
            mask = mask[0].mul(255).byte().cpu().numpy()  # Convert the mask to a binary image
            white_background = np.ones_like(image_np) * 255  # Create a white background
            segmented_image = np.where(mask[:, :, np.newaxis] > 0, image_np, white_background)  # Apply the mask
            object_image = Image.fromarray(segmented_image.astype(np.uint8))  # Convert to PIL image
            object_image.save(os.path.join(output_dir, f"{os.path.splitext(image_filename)[0]}_object_{i}.png"))
            print(f"Saved {os.path.splitext(image_filename)[0]}_object_{i}.png")

def process_images(input_folder, output_folder):
    """
    Process images in the input folder, perform object detection and segmentation, and save the results.
    
    Args:
        input_folder (str): Directory containing input images.
        output_folder (str): Directory where segmented objects will be saved.
    """
    # Iterate over all files in the input folder
    for image_filename in os.listdir(input_folder):
        if image_filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(input_folder, image_filename)
            image = Image.open(image_path).convert('RGB')  # Open and convert image to RGB
            image = resize_image(image)  # Resize image
            image_tensor = transform(image).unsqueeze(0)  # Convert image to tensor
            image_tensor = image_tensor.to(device)  # Move tensor to appropriate device
            with torch.no_grad():  # Disable gradient calculation
                predictions = model(image_tensor)  # Get model predictions
            save_segmented_objects(image, predictions, image_filename, output_dir=output_folder)  # Save segmented objects

def run_segmentation(input_images_path, segmented_objects_path):
    """
    Run the segmentation process on the input images.
    
    Args:
        input_images_path (str): Path to the input images directory.
        segmented_objects_path (str): Path to the directory where segmented objects will be saved.
    """
    process_images(input_images_path, segmented_objects_path)

if __name__ == "__main__":
    # Define paths
    input_folder = '../data/input_images'
    output_folder = '../data/segmented_objects'
    
    # Run the segmentation process
    run_segmentation(input_folder, output_folder)
