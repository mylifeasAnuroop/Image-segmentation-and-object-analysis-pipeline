import unittest
import os
import json
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory of the 'tests' folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.text_extraction_model import TextExtractionModel

class TestTextExtractionModel(unittest.TestCase):
    def setUp(self):
        # Initialize the TextExtractionModel
        self.model = TextExtractionModel()

        # Mock metadata
        self.mock_metadata = [
            {
                "image_id": "test_image_1.png",
                "detection": {"description": "test_object_1", "probability": 0.9},
                "texts": "- no text found"
            }
        ]

        # Create a mock segmented image
        self.mock_image_path = os.path.join(self.model.segmented_object_dir, 'test_image_1.png')
        os.makedirs(self.model.segmented_object_dir, exist_ok=True)
        with open(self.mock_image_path, 'w') as f:
            f.write('mock image data')

        # Create a mock metadata file
        self.metadata_path = self.model.metadata_file
        os.makedirs(os.path.dirname(self.metadata_path), exist_ok=True)
        with open(self.metadata_path, 'w') as f:
            json.dump(self.mock_metadata, f, indent=4)

    def tearDown(self):
        # Clean up the mock files and directories after tests
        if os.path.exists(self.mock_image_path):
            os.remove(self.mock_image_path)
        if os.path.exists(self.metadata_path):
            os.remove(self.metadata_path)
        if os.path.exists(self.model.segmented_object_dir):
            os.rmdir(self.model.segmented_object_dir)
        if os.path.exists(os.path.dirname(self.metadata_path)):
            os.rmdir(os.path.dirname(self.metadata_path))

    @patch('cv2.imread', return_value=None)
    def test_extract_text_empty_image(self, mock_imread):
        # Test the extract_text method with an empty image
        extracted_text = self.model.extract_text(self.mock_image_path)
        self.assertEqual(extracted_text, "", "Expected no text extracted from an empty image")

    @patch('cv2.imread')
    @patch('easyocr.Reader.readtext')
    def test_extract_text_valid_image(self, mock_readtext, mock_imread):
        # Mock a valid image and OCR result
        mock_imread.return_value = MagicMock()
        mock_readtext.return_value = [(0, "test text", 0.99)]
        
        extracted_text = self.model.extract_text(self.mock_image_path)
        self.assertEqual(extracted_text, "test text", "Expected extracted text to be 'test text'")

    @patch('models.text_extraction_model.TextExtractionModel.extract_text', return_value="extracted text")
    def test_process_objects(self, mock_extract_text):
        # Test the process_objects method to ensure metadata is updated correctly
        self.model.process_objects()

        # Reload the metadata to check updates
        with open(self.metadata_path, 'r') as f:
            updated_metadata = json.load(f)

        # Ensure the text was updated in the metadata
        self.assertEqual(updated_metadata[0]['texts'], "extracted text", "Expected 'extracted text' in metadata")

if __name__ == "__main__":
    unittest.main()
