import sys
import os
import unittest
from PIL import Image
import cv2
import numpy as np

# Add the parent directory of the current script to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the segmentation model from the models directory
from models.segmentation_model import (
    ensure_pretrained_models,
    load_yolo_model,
    load_image,
    convert_bgr_to_rgb,
    load_sam_model,
    apply_segmentation_mask,
    save_segmented_object,
    process_images_in_directory,
    segment_objects
)

class TestSegmentationModel(unittest.TestCase):

    def setUp(self):
        # Set up paths
        self.weights_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'weights')
        self.input_images_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'input_images')
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'segmented_objects')
        self.yolo_model_path = os.path.join(self.weights_dir, "yolov8n.pt")
        self.sam_checkpoint_path = os.path.join(self.weights_dir, "sam_vit_h_4b8939.pth")
        
        # Ensure pretrained models are available
        ensure_pretrained_models(self.weights_dir)
        
        # Load models
        self.yolo_model = load_yolo_model(self.yolo_model_path)
        self.sam_predictor = load_sam_model(self.sam_checkpoint_path, "vit_h")
        
        # Automatically select the first image in the input_images_dir
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        self.test_image_path = None
        for file in os.listdir(self.input_images_dir):
            if file.lower().endswith(valid_extensions):
                self.test_image_path = os.path.join(self.input_images_dir, file)
                break
        
        if not self.test_image_path:
            self.fail("No valid image found in the input_images directory for testing")
        
        # Load a test image
        self.image = load_image(self.test_image_path)
        self.image_rgb = convert_bgr_to_rgb(self.image)
        
    def test_model_loading(self):
        # Test if YOLO and SAM models are loaded properly
        self.assertIsNotNone(self.yolo_model, "Failed to load YOLO model")
        self.assertIsNotNone(self.sam_predictor, "Failed to load SAM model")
    
    def test_image_loading(self):
        # Test if the test image is loaded correctly
        self.assertEqual(self.image.shape[0] > 0, True, "Failed to load test image")
        self.assertEqual(self.image.shape[1] > 0, True, "Failed to load test image")
    
    def test_segmentation_process(self):
        # Process the image and check the segmentation output
        self.sam_predictor.set_image(self.image_rgb)
        
        # Use YOLO to predict objects
        results = self.yolo_model.predict(source=self.test_image_path, conf=0.25)
        
        object_id = 1
        for result in results:
            for box in result.boxes:
                bbox = box.xyxy.tolist()  # Extract bounding box coordinates
                input_box = np.array(bbox)
                
                masks, _, _ = self.sam_predictor.predict(
                    point_coords=None,
                    point_labels=None,
                    box=input_box[None, :],
                    multimask_output=False,
                )
                
                segmented_image = apply_segmentation_mask(self.image_rgb, masks[0])
                output_path = os.path.join(self.output_dir, f"{os.path.splitext(os.path.basename(self.test_image_path))[0]}_object_{object_id}.png")
                save_segmented_object(segmented_image, output_path)
                
                # Check if the segmented image was saved correctly
                self.assertTrue(os.path.isfile(output_path), f"Segmented image not saved: {output_path}")
                object_id += 1

if __name__ == "__main__":
    unittest.main()


