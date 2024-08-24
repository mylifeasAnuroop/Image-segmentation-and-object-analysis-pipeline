import os
import json
import warnings
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

class IdentificationModel:
    """
    A class to perform object identification using the CLIP model.
    """

    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        """
        Initializes the IdentificationModel with the CLIP model and processor.
        Sets device to GPU if available, otherwise CPU.
        """
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Set the relative path for segmented objects and metadata
        self.segmented_object_dir = os.path.join(script_dir, '../data/segmented_objects')
        self.metadata_file = os.path.join(script_dir, '../data/output/metadata.json')
        
        # Load the CLIP model and processor
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def identify_objects(self, image_path, text_descriptions):
        """
        Identifies objects in a given image using text descriptions.
        
        Args:
            image_path (str): The path to the image file.
            text_descriptions (list): A list of text descriptions to match with the image.
        
        Returns:
            dict or None: A dictionary with the description and probability of the identified object,
                          or None if no object is identified with a probability greater than 0.25.
        """
        try:
            # Load image
            image = Image.open(image_path)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None

        # Prepare inputs
        inputs = self.processor(text=text_descriptions, images=image, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Get logits and compute probabilities
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)

        # Find the detection with the maximum probability
        max_prob, max_idx = torch.max(probs[0], dim=0)

        # Only consider the detection if its probability is greater than 0.25 (25%)
        if max_prob > 0.25:
            return {
                'description': text_descriptions[max_idx],
                'probability': float(max_prob)
            }
        else:
            return None

    def process_directory(self, text_descriptions):
        """
        Processes all images in the segmented objects directory and identifies objects.
        
        Args:
            text_descriptions (list): A list of text descriptions to match with the images.
        """
        metadata = []

        # Iterate through all files in the segmented objects directory
        for filename in os.listdir(self.segmented_object_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.segmented_object_dir, filename)
                
                # Identify the objects in the image
                detection = self.identify_objects(image_path, text_descriptions)
                
                # Add metadata entry only if detection is not None
                if detection is not None:
                    metadata.append({
                        'image_id': filename,
                        'detection': detection
                    })

        # Save the metadata to a file
        self.save_metadata(metadata)

    def save_metadata(self, metadata):
        """
        Saves the metadata to a JSON file.
        
        Args:
            metadata (list): A list of metadata entries to save.
        """
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)

        # Save metadata as JSON
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=4)
            print(f"Metadata saved to {self.metadata_file}")
        except Exception as e:
            print(f"Error saving metadata: {e}")

def run_identification(segmented_objects_path, metadata_file):
    """
    Runs the object identification process with specified paths.
    
    Args:
        segmented_objects_path (str): The path to the directory containing segmented objects.
        metadata_file (str): The path to the file where metadata will be saved.
    """
    model = IdentificationModel()
    text_descriptions = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                         'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
                         'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
                         'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
                         'baseball bat', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                         'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
                         'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant',
                         'bed', 'dining table', 'toilet', 'TV', 'laptop', 'mouse', 'remote', 'keyboard',
                         'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
                         'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
    model.segmented_object_dir = segmented_objects_path
    model.metadata_file = metadata_file
    model.process_directory(text_descriptions)

# Usage
if __name__ == "__main__":
    run_identification('../data/segmented_objects', '../data/output/metadata.json')
