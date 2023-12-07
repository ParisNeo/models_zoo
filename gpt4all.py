import json
import requests
import yaml
from pathlib import Path

def fetch_json_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch JSON from URL. Status code: {response.status_code}")

def convert_to_yaml(json_entry):
    yaml_entry = {
        "category": "generic",
        "datasets": None,  # You can fill this in based on your requirements
        "last_commit_time": None,  # You can fill this in based on your requirements
        "license": "apache-2.0",
        "model_creator": "Mistral + OpenOrca",
        "model_creator_link": "akjindal53244",
        "name": json_entry["filename"],
        "description": json_entry["description"],
        "quantizer": "TheBloke",
        "rank": 10000000000.0,
        "type": "gpt4all",
        "server": json_entry["url"],
        "variants": [
            {
                "name": json_entry["filename"],
                "size": int(json_entry["filesize"])
            }
        ]
    }

    return yaml_entry

# URL for the JSON data
json_url = "https://raw.githubusercontent.com/nomic-ai/gpt4all/main/gpt4all-chat/metadata/models2.json"

# Fetch JSON data from the URL
json_data = fetch_json_from_url(json_url)

# Process each entry in the JSON data
yaml_entries = [convert_to_yaml(entry) for entry in json_data]

# Get the path to the current script
script_path = Path(__file__).resolve().parent

# Save YAML to a file in the same folder
yaml_file_path = script_path / "gpt4all.yaml"
with open(yaml_file_path, "w") as yaml_file:
    yaml.dump(yaml_entries, yaml_file, default_flow_style=False)

print(f"YAML file saved at: {yaml_file_path}")
