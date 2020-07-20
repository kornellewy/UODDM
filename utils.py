#TODO: komentarze
import os
import shutil
import cv2
from math import pi
import numpy as np
import pprint
import glob

def print_list_of_dict(list_of_dict):
    """
    Fuction print all dict in list one after another.
    :param list_of_dict: list of dict to print
    :type list_of_dict: str or numpy ndarray
    :retruns: None
    :rtype: None
    """
    for i_dict in list_of_dict:
        pprint.pprint(i_dict)
    return None

def get_image_size(img):
    """
    Return width, height of image.
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
    """
    Function return image name from path u give.
    :param path: path to img
    :type path: str
    :retruns: None
    :rtype: None
    """
    _, name = os.path.split(path)
    name, _ = os.path.splitext(name)
    return name

def load_images_names(path):
    """
    Function return list of images names in path folder u give.
    Name so with no tail path and extencion.
    :param path: path to folder with images
    :type path: str
    :retruns: list of founded images names.
    :rtype: list
    """
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
    """
    Function return list of images names in path folder u give.
    Name so with no extecion.
    :param path: path to folder with images
    :type path: str
    :retruns: list of founded images names.
    :rtype: list
    """
    images = []
    valid_images = [".jpg", ".png", "jpeg"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_images:
            continue
        images.append(file)
    return images

def find_all_dirs(path):
    """
    Function find all folders in given path.
    :param path: path to folder with subfolders
    :type path: str
    :retruns: list of fouded folders
    :rtype: list
    """
    return [ f.path for f in os.scandir(path) if f.is_dir() ]

def find_all_dirs_names(path):
    """
    Function find all folders names in given path.
    :param path: names folders with subfolders
    :type path: str
    :retruns: list of fouded folders
    :rtype: list
    """
    return [ os.path.split(f.path)[1] for f in os.scandir(path) if f.is_dir() ]

def find_all_jpg(path):
    """
    Funcion find all jpegs in given folder and it subfoldrs. 
    :param path: path to folder with subfolders and jpegs
    :type path: str
    :retruns: list of fouded images
    :rtype: list
    """
    images = []
    for x in os.walk(path):
        for y in glob.glob(os.path.join(x[0], '*.jpg')):
            images.append(y)
    return images

def clean_tmp(path):
    """
    That method clean tmp dir.
    :param path: path to dir
    :type path: str
    :retruns: None
    :rtype: None
    """
    if not os.path.exists(path):
        os.mkdir(path)
    shutil.rmtree(path)
    os.mkdir(path)
    return None

def remove_folder(path):
    """
    Remove folder in given path.
    :param path: path to dir
    :type path: str
    :retruns: None
    :rtype: None
    """
    shutil.rmtree(path)
    return None

def load_images(path):
    """
    Function return list of images paths in path folder u give.
    :param path: path to folder with images
    :type path: str
    :retruns: list of founded images paths.
    :rtype: list
    """
    images = []
    valid_images = [".jpg", ".png", ".jpeg"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_images:
            continue
        images.append(os.path.join(path, f))
    return images

def load_images_gen(path):
    """
    Function return list of images paths in path folder u give (using generator).
    :param path: path to folder with images
    :type path: str
    :retruns: list of founded images paths.
    :rtype: list
    """
    valid_images = [".jpg", ".png", "jpeg"]
    for root, dirs, files in os.walk(path):
        for file_name in files:
            name, ext = os.path.splitext(file_name)
            if ext.lower() not in valid_images:
                continue
            yield os.path.join(root, file_name)

def load_text_files(path):
    """
    Function return list of txts paths in path folder u give.
    :param path: path to folder with txts
    :type path: str
    :retruns: list of founded txts paths.
    :rtype: list
    """
    txts = []
    valid_txts = [".txt"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_txts:
            continue
        txts.append(os.path.join(path, f))
    return txts