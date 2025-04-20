import requests
from bs4 import BeautifulSoup
import yaml

def scrape_model_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    models = []
    # Find the first table in the document
    table = soup.find('table')
    if not table:
        print("No table found in the HTML.")
        return models

    rows = table.find_all('tr')[1:]  # Skip header row
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 4:
            model_name = cols[0].text.strip()
            anthropic_api = cols[1].text.strip()
            aws_bedrock = cols[2].text.strip()
            gcp_vertex_ai = cols[3].text.strip()
            
            # Use the Anthropic API name as the model name
            model_name = anthropic_api.split('(')[0].strip()
            
            model = {
                'category': 'generic',
                'datasets': 'unknown',
                'icon': '/bindings/anthropic_llm/Anthropic.png',
                'last_commit_time': None,
                'license': 'commercial',
                'model_creator': 'anthropic',
                'model_creator_link': 'https://anthropic.com',
                'name': model_name,
                'provider': None,
                'rank': 1.0,
                'type': 'api',
                'variants': [{
                    'name': model_name,
                    'size': None,
                    'ctx_size': 200000,
                    'max_n_predict': 4096,
                    'input_cost': 3.0,
                    'output_cost': 15.0
                }]
            }
            models.append(model)
    
    return models

def write_yaml(data, filename):
    with open(filename, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)

# URL of the page to scrape (replace with actual URL)
url = 'https://docs.anthropic.com/en/docs/about-claude/models'

# Scrape the data
model_data = scrape_model_data(url)

# Write to YAML file
write_yaml(model_data, 'anthropic.yaml')

print("YAML file has been created: anthropic.yaml")
