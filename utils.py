import os

def load_images_without_extention(path):
    images = []
    valid_images = [".jpg", ".png", "jpeg"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_images:
            continue
        images.append(file)
    return images