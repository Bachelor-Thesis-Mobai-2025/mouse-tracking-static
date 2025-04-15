import json
import glob
import os

# Paths to the folders containing the JSON files
truthful_folder = "data/truthful_responses/"
deceptive_folder = "data/deceptive_responses/"

def add_labels_to_json_files(folder, label):
    """Add label to each JSON file based on its folder."""
    files = glob.glob(folder + "*.json")
    for file_path in files:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Add label to the data
        data["label"] = label
        
        # Save the updated JSON file with the label
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Added label {label} to {file_path}")

# Add labels to truthful and deceptive files
add_labels_to_json_files(truthful_folder, 0)  # 0 for truthful
add_labels_to_json_files(deceptive_folder, 1)  # 1 for deceptive
