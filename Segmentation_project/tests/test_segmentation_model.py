import os
import sys
import unittest

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.segmentation_model import run_segmentation

class TestSegmentation(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment. This method is called before each test.
        """
        self.input_folder = '../data/input_images'
        self.output_folder = '../data/segmented_objects'

        # Ensure the output directory is clean before running the test
        if os.path.exists(self.output_folder):
            for filename in os.listdir(self.output_folder):
                file_path = os.path.join(self.output_folder, filename)
                os.remove(file_path)
        else:
            os.makedirs(self.output_folder)

    def test_segmentation(self):
        """
        Test the segmentation process.
        """
        # Run the segmentation process
        run_segmentation(self.input_folder, self.output_folder)
        
        # Verify that the output directory is not empty
        self.assertGreater(len(os.listdir(self.output_folder)), 0, "No segmented objects were saved.")

if __name__ == "__main__":
    unittest.main()
