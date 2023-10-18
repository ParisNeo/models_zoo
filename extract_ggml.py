import yaml
from pathlib import Path
def extract_entries(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    
    entries = []
    for entry in data:
        name = entry.get('name', '').lower()
        if 'gguf' in name:
            entries.append(entry)
    
    return entries

file_path = Path(__file__).parent/'gguf.yaml'
entries = extract_entries(file_path)

output_file = Path(__file__).parent/'output_gguf.yaml'
with open(output_file, 'w') as file:
    yaml.dump(entries, file)