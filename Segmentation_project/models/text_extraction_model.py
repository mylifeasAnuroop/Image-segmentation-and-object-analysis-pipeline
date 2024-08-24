
import os
import cv2
import easyocr
import warnings
import json

# Suppress warnings
warnings.filterwarnings("ignore")

class TextExtractionModel:
    def __init__(self):
        # Initialize the OCR reader for the English language
        self.reader = easyocr.Reader(['en'])
        
        # Define paths to directories and files relative to the script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.segmented_object_dir = os.path.join(script_dir, '../data/segmented_objects')  # Directory containing segmented object images
        self.input_images_dir = os.path.join(script_dir, '../data/input_images')  # Directory containing input images (not used in the current implementation)
        self.metadata_file = os.path.join(script_dir, '../data/output/metadata.json')  # File path for metadata JSON

    def extract_text(self, image_path):
        """
        Extract text from an image using OCR.
        
        Args:
            image_path (str): Path to the image file from which text will be extracted.
        
        Returns:
            str: Extracted text from the image.
        """
        try:
            # Read the image from the specified path
            img = cv2.imread(image_path)
            
            # Check if the image was read successfully
            if img is None or img.size == 0:
                print(f"Warning: Empty or invalid image at {image_path}")
                return ""

            # Check if the image dimensions are too small
            if img.shape[0] < 10 or img.shape[1] < 10:
                print(f"Warning: Image too small at {image_path}")
                return ""

            # Perform Optical Character Recognition (OCR) on the image
            results = self.reader.readtext(img)
            
            # Extract and concatenate all recognized texts
            extracted_text = ' '.join([result[1] for result in results])
            
            return extracted_text
        except Exception as e:
            # Handle any exceptions that occur during text extraction
            print(f"Error processing image at {image_path}: {str(e)}")
            return ""

    def process_objects(self):
        """
        Process segmented object images, extract text from them, and update the metadata file.
        """
        # Load metadata from JSON file
        with open(self.metadata_file, 'r') as f:
            metadata = json.load(f)
        
        for entry in metadata:
            # Extract object ID from image_id field
            object_id = entry['image_id'].split('.')[0]
            # Construct the path to the segmented object image
            object_image = os.path.join(self.segmented_object_dir, f"{object_id}.png")
            
            # Extract text from the segmented object image
            extracted_text = self.extract_text(object_image)
            
            # Update metadata entry with the extracted text
            if extracted_text:
                entry['texts'] = extracted_text
            else:
                entry['texts'] = "- no text found"
        
        # Save the updated metadata back to the JSON file
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)

        # Print a confirmation message
        print(f"Metadata updated with extracted text in {self.metadata_file}")

def run_text_extraction():
    """
    Function to run the text extraction process using the TextExtractionModel.
    """
    model = TextExtractionModel()
    model.process_objects()

# Example usage
if __name__ == "__main__":
    run_text_extraction()
