"""
Upload dataset to the langfuse.

Usage:
    python upload-dataset.py <dataset_name> items.json
"""
import tqdm
import json
import argparse
import dotenv
from langfuse import Langfuse

dotenv.load_dotenv()
langfuse = Langfuse()

def add_item(dataset_name, item):
    langfuse.create_dataset_item(
        dataset_name=dataset_name,
        # any python object or value, optional
        input=item.pop("input"),
        # any python object or value, optional
        expected_output=item.pop("expected_output"),
        # metadata, optional
        metadata=item,
    )


def main():
    parser = argparse.ArgumentParser(description="Upload dataset to langfuse.")
    parser.add_argument("dataset_name", type=str, help="Name of the dataset")
    parser.add_argument("items_file", type=argparse.FileType("r"),
                        help="Path to the JSON file containing items")
    args = parser.parse_args()

    # Read items from JSON file
    items = json.load(args.items_file)

    # Upload each item to the dataset
    for item in tqdm.tqdm(items):
        add_item(args.dataset_name, item)


if __name__ == "__main__":
    main()
