import requests
import os

def save_image(url: str, output_dir: str = "images") -> str:
    os.makedirs(output_dir, exist_ok=True)
    image_number = len(os.listdir(output_dir)) + 1
    filename = f"picture{image_number}.png"
    filepath = os.path.join(output_dir, filename)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(response.content)
        return filepath
    except requests.exceptions.RequestException:
        return None
