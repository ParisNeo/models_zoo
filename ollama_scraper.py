import requests
from bs4 import BeautifulSoup
import json

def is_meta_model(model_name):
    # List of known Meta models
    meta_models = ['llama', 'codellama', 'llama-guard']
    return any(model.lower() in model_name.lower() for model in meta_models)

def scrape_ollama_models():
    url = "https://ollama.com/library"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"[DEBUG] Fetching URL: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all h2 elements
    all_h2 = soup.find_all('h2')
    print(f"[DEBUG] Processing {len(all_h2)} h2 elements")
    
    models_list = []
    
    for h2 in all_h2:
        model_name = h2.text.strip()
        if model_name:  # Skip empty model names
            print(f"[DEBUG] Processing model: {model_name}")
            
            # Determine ownership
            owned_by = "meta" if is_meta_model(model_name) else "community"
            
            models_list.append({
                "model_name": f"{model_name}:latest",
                "owned_by": owned_by
            })
            # Also add version without ":latest"
            models_list.append({
                "model_name": model_name,
                "owned_by": owned_by
            })
    
    # Save to file
    output_file = "ollama_models.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(models_list, f, indent=4)
    print(f"[DEBUG] Saved models to {output_file}")
    
    return models_list

# Run the scraper
if __name__ == "__main__":
    models_list = scrape_ollama_models()
    print(f"\n[DEBUG] Processed {len(models_list)} models in total")
