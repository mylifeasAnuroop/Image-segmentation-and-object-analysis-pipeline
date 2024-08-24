import unittest
import os
import json
import sys
import numpy as np
from PIL import Image
from io import BytesIO
from models.identification_model import IdentificationModel

# Add the parent directory of the 'tests' folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestIdentificationModel(unittest.TestCase):
    def setUp(self):
        # Initialize the IdentificationModel
        self.model = IdentificationModel()
        
        # Create a mock text description list
        self.text_descriptions = ['person', 'dog', 'cat', 'bottle', 'car', 'bicycle']
        
        # Generate a simple test image (a white square)
        self.test_image = Image.fromarray(np.ones((224, 224, 3), dtype=np.uint8) * 255)
        
        # Mock paths
        self.test_image_path = os.path.join(self.model.segmented_object_dir, 'test_image.png')
        self.metadata_file = self.model.metadata_file
        
        # Save the test image to the segmented_objects directory
        os.makedirs(self.model.segmented_object_dir, exist_ok=True)
        self.test_image.save(self.test_image_path)

    def tearDown(self):
        # Clean up the test image and metadata file after tests
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.metadata_file):
            os.remove(self.metadata_file)

    def test_identify_objects(self):
        # Test the identification of objects in the test image
        detection = self.model.identify_objects(self.test_image_path, self.text_descriptions)
        
        # Since the image is just a white square, we expect no detection
        self.assertIsNone(detection, "Expected no detection for a plain white image")

    def test_process_directory(self):
        # Test processing the directory and saving metadata
        self.model.process_directory(self.text_descriptions)
        
        # Check if the metadata file was created
        self.assertTrue(os.path.exists(self.metadata_file), "Metadata file should be created")
        
        # Load the metadata and check its content
        with open(self.metadata_file, 'r') as f:
            metadata = json.load(f)
        
        # Since the image is just a white square, we expect no entries in the metadata
        self.assertEqual(len(metadata), 0, "Expected no metadata entries for a plain white image")

if __name__ == "__main__":
    unittest.main()
