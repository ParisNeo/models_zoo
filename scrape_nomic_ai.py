# Project: JSON to YAML converter
# author: ParisNeo

import argparse
import json
import yaml
from datetime import datetime
import requests
from pathlib import Path

def convert_json_to_yaml(json_path, yaml_path):
    # Read the JSON file
    if json_path.startswith('http'): # If JSON path is a URL
        response = requests.get(json_path)
        data = response.json()
    else: # If JSON path is a local file
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

    # Create the YAML data
    yaml_data = []
    for item in data:
        yaml_item = {
            'category': 'generic',  # If you have a different category by default, put it here as the JSON has no categories
            'datasets': [],  # No datasets field found in the JSON
            'icon': 'https://cdn.gptfrance.ai/storage/2023/06/gpt4all-128.png',  # No icon found in the JSON, so please put a default one
            'last_commit_time': datetime.now(),  # No commit time found in the JSON, so using the current time
            'license': '',
            'model_creator':  item["url"].split("/")[3] if "url" in list(item.keys()) else "",  # Extracting the model creator from the JSON
            'model_creator_link': "/".join(item["url"].split("/")[:4]) if "url" in list(item.keys()) else "",  # Extracting the model creator link from the JSON
            'name': item["url"].split("/")[4] if "url" in list(item.keys()) else "",  # Extracting the name from the JSON
            'provider': item.get('provider', ''),  # Extracting the provider from the JSON
            'rank': 10000000000.0,
            'type': item.get('type', ''),  # Extracting the type from the JSON
            'variants': [
                {
                    "name": item.get('filename', ''),  # Extracting the filename from the JSON
                    "size": item.get('filesize', '')  # Extracting the filesize from the JSON
                }
            ]
        }
        # Now let's add this entry to the yaml_data
        yaml_data.append(yaml_item)

    # Write the YAML data to file
    with open(yaml_path, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file)

# Set up argparse to handle command line arguments
parser = argparse.ArgumentParser(description='Convert JSON to YAML')
parser.add_argument('--json_path', default='https://raw.githubusercontent.com/nomic-ai/gpt4all/main/gpt4all-chat/metadata/models.json', help='Path to the JSON file')
parser.add_argument('--yaml_path', default=Path(__file__).parent/'nomicai.yaml', help='Path to save the YAML file')

args = parser.parse_args()

# Usage example
convert_json_to_yaml(args.json_path, args.yaml_path)
