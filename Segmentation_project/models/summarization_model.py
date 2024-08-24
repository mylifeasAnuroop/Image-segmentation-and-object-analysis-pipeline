import json
from transformers import pipeline
import warnings

# Suppress warnings to avoid cluttering the output
warnings.filterwarnings("ignore")

class SummarizationModel:
    def __init__(self, metadata_file_path):
        """
        Initialize the SummarizationModel with the path to the metadata file.

        Args:
            metadata_file_path (str): Path to the metadata JSON file.
        """
        # Initialize the summarization pipeline from transformers
        self.summarizer = pipeline("summarization")
        self.metadata_file = metadata_file_path

    def summarize_text(self, text):
        """
        Summarize the provided text using the summarization pipeline.

        Args:
            text (str): Text to be summarized.

        Returns:
            str: Summary of the provided text.
        """
        try:
            # Perform summarization
            summary = self.summarizer(text, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
            return summary
        except Exception as e:
            print(f"Error summarizing text: {str(e)}")
            return None

    def process_metadata(self):
        """
        Load metadata, summarize texts, and save updated metadata.
        """
        try:
            # Load the metadata from the JSON file
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)

            # Process each entry in the metadata
            for entry in metadata:
                if 'texts' in entry:
                    text_content = entry['texts']

                    # Initialize the summary category if it does not exist
                    if 'summary' not in entry:
                        entry['summary'] = None

                    # Summarize the text if it exists and is not a placeholder
                    if text_content and text_content != '- no text found':
                        entry['summary'] = self.summarize_text(text_content)
                    else:
                        entry['summary'] = "NA"

            # Save the updated metadata back to the JSON file
            self.save_metadata(metadata)

        except Exception as e:
            print(f"Error processing metadata: {str(e)}")

    def save_metadata(self, metadata):
        """
        Save the updated metadata back to the JSON file.

        Args:
            metadata (dict): The updated metadata to be saved.
        """
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=4)
            print(f"Metadata successfully saved to {self.metadata_file}")
        except Exception as e:
            print(f"Error saving metadata: {str(e)}")

def run_summarization(metadata_file_path):
    """
    Run the summarization process using the SummarizationModel.

    Args:
        metadata_file_path (str): Path to the metadata JSON file.
    """
    model = SummarizationModel(metadata_file_path)
    model.process_metadata()

# Example usage
if __name__ == "__main__":
    # Path to the metadata file
    metadata_file_path = r'../data/output/metadata.json'
    run_summarization(metadata_file_path)
