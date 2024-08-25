import os
import sys
import unittest

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.identification_model import run_identification

class TestIdentificationModel(unittest.TestCase):
    
    def setUp(self):
        self.input_folder = '../data/segmented_objects'
        self.output_folder = '../data/output'
        self.metadata_file = os.path.join(self.output_folder, 'metadata.json')

        # Ensure the output folder exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def test_identification(self):
        # Run the identification process
        run_identification(self.input_folder, self.metadata_file)
        
        # Verify that the metadata file was created and is not empty
        self.assertTrue(os.path.isfile(self.metadata_file), "Metadata file was not created.")
        
        # Check if the metadata file is not empty
        with open(self.metadata_file, 'r') as file:
            data = file.read()
            self.assertGreater(len(data), 0, "Metadata file is empty.")
    
    def tearDown(self):
        # Clean up: Remove the metadata file after test
        if os.path.isfile(self.metadata_file):
            os.remove(self.metadata_file)

if __name__ == "__main__":
    unittest.main()
