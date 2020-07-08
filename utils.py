import os
import shutil

def load_images(path):
    images = []
    valid_images = [".jpg", ".png", "jpeg"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_images:
            continue
        images.append(f)
    return images

def load_images_without_extention(path):
    images = []
    valid_images = [".jpg", ".png", "jpeg"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_images:
            continue
        images.append(file)
    return images

def clean_tmp(path):
    """That method clean tmp dir.
    :param path: path to emp dir
    :type path: str
    :retruns: None
    :rtype: None
    """
    shutil.rmtree(path)
    os.mkdir(path)
    return None