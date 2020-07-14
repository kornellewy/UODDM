#TODO: komentarze
import os
import shutil
import cv2
from math import pi
import numpy as np

def get_image_size(img):
    """ Return width, height of image.
    :param img_path: path to image on dirve or img numpy ndarray
    :type img_path: str or numpy ndarray
    :retruns: width, height of img
    :rtype: tuple
    """
    if isinstance(img, str):
        img = cv2.imread(img)
    elif isinstance(img, np.ndarray):
        pass
    height, width, depth = img.shape
    return width, height, depth

def get_rad(theta, phi, gamma):
    """
    Function that convert all rotation angles in degrees to radians.
    :param theta: number of degres in cordination system
    :type theta: float or int
    :param phi: number of degres in cordination system
    :type phi: float or int
    :param gamma: number of degres in cordination system
    :type gamma: float or int
    :retruns: tuple of floats taht are radians of angle.
    :rtype: tuple
    """
    return (deg_to_rad(theta),
            deg_to_rad(phi),
            deg_to_rad(gamma))

def deg_to_rad(deg):
    """
    Function that convert angle in degrees to radians.
    :param deg: number of degres
    :type deg: float or int
    :retruns: number of radians
    :rtype: float
    """
    return deg * pi / 180.0

def get_image_name(path):
    #TODO: komentarze
    _, name = os.path.split(path)
    name, _ = os.path.splitext(name)
    return name

def load_images_names(path):
    #TODO: komentarze
    images = []
    valid_images = [".jpg", ".png", "jpeg"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_images:
            continue
        _, name = os.path.split(file)
        images.append(name)
    return images

def load_images_without_extention(path):
    #TODO: komentarze
    images = []
    valid_images = [".jpg", ".png", "jpeg"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_images:
            continue
        images.append(file)
    return images

def find_all_dir(path):
    #TODO: komentarze
    return [ f.path for f in os.scandir(path) if f.is_dir() ]

def find_all_jpg(path):
    #TODO: komentarze
    images = []
    for x in os.walk(path):
        for y in glob.glob(os.path.join(x[0], '*.jpg')):
            images.append(y)
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

def remove_folder(path):
    shutil.rmtree(path)
    return None

def load_images(path):
    #TODO: komentarze
    images = []
    valid_images = [".jpg", ".png", ".jpeg"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_images:
            continue
        images.append(os.path.join(path, f))
    return images

def load_images_gen(path):
    #TODO: komentarze
    valid_images = [".jpg", ".png", "jpeg"]
    for root, dirs, files in os.walk(path):
        for file_name in files:
            name, ext = os.path.splitext(file_name)
            if ext.lower() not in valid_images:
                continue
            yield os.path.join(root, file_name)



if __name__ == "__main__":
    print(list(x**2 for x in range(10)))
