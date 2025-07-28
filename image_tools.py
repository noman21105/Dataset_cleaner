import os
from PIL import Image

def resize_images_recursive(folder_path, size=(224, 224)):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(root, file)
                try:
                    with Image.open(path) as img:
                        img = img.resize(size)
                        img.save(path)
                except Exception:
                    pass  # Skip corrupted files

def delete_unwanted_formats_recursive(folder_path, formats_to_delete):
    deleted = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in formats_to_delete):
                try:
                    os.remove(os.path.join(root, file))
                    deleted += 1
                except Exception:
                    pass
    return deleted
