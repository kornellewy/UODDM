"""
Module agument object detection dataset by artifical generation images and labels.
"""
import os
import cv2
import random
import numpy as np
from scipy import ndimage
import math
from PIL import Image

from utils import load_images, load_images_names, get_image_name, get_image_size, remove_folder
from pascal_dataset_maker import PascalDatasetWriter
from data_argumentation_utils import DataRandomModifier

class PascalDataAugmenter(PascalDatasetWriter):
    def __init__(self, tmp_folder='tmp', min_cut_img_count = 1,max_cut_img_count = 5,background_image_width = 1920,background_image_height = 1080, background_image_depth = 3):
        """
        The task of class is to argument pascal type object detecion dataset. 
        First that class save unchange data that gets in uniform data format. 
        U can see that format in labelbox_interface.py on end of pipeline.
        After saving class cut object form original data to saperate folders, 
        then take background photos and cut object and to both apply saparete transforms.
        (_background_image_transform, _cut_image_transform). In the end we paste transformed
        images on transformed background. When we paste we got location and size on original image
        and we save that like normal data.
        """
        super().__init__()
        self.dataset_classes_path_map = dict()
        self.image_random_modifier = DataRandomModifier()
        self.tmp_folder = tmp_folder
        self.min_cut_img_count = min_cut_img_count
        self.max_cut_img_count = max_cut_img_count
        self.background_image_width = background_image_width
        self.background_image_height = background_image_height
        self.background_image_depth = background_image_depth

    def _background_image_transform(self, image):
        """
        Method that random transform background image.
        :param image: background image to random transform
        :type image: numpy ndarray
        :retruns: transform image
        :rtype: numpy ndarray
        """
        image = self.image_random_modifier.random_crop(image)
        image = self.image_random_modifier.random_horizontal_filp(image)
        image = self.image_random_modifier.random_vertical_filp(image)
        image = self.image_random_modifier.random_channel_swap(image)
        image = self.image_random_modifier.random_blur(image, 0.3)
        image = self.image_random_modifier.random_gaussian_noise(image, 0.1)
        image = self.image_random_modifier.random_img_to_gray(image, 0.1)
        return image

    def _cut_image_transform(self, image):
        """
        Method that random transform cut image (object).
        :param image: cut image to random transform
        :type image: numpy ndarray
        :retruns: transform image
        :rtype: numpy ndarray
        """
        image = self.image_random_modifier.random_channel_swap(image)
        image = self.image_random_modifier.random_blur(image, 0.3)
        image = self.image_random_modifier.random_gaussian_noise(image, 0.1)
        image = self.image_random_modifier.random_img_to_gray(image, 0.1)
        return image

    def _create_tmp_structure(self):
        """
        Method create tmp folders for storin cut images (objct) of difrend classes.
        :retruns: None
        :rtype: None
        """
        for key, value in self.dataset_classes_map.items():
            class_folder_path = os.path.join(self.dataset_folder_path, key)
            if not os.path.exists(class_folder_path):
                os.mkdir(class_folder_path)
            self.dataset_classes_path_map.update({key: class_folder_path})
        return None

    def _cut_objects(self, image_data):
        """
        Method cut labled objcet form image and save it as small image in tmp class folders.
        :param image_data: dict of info about image and all object on that image
        :type image_data: dict
        :retruns: None
        :rtype: None
        """
        full_image = cv2.imread(image_data['img_path'])
        width, height, depth = get_image_size(full_image)
        if height>width:
            full_image = ndimage.rotate(full_image , 90)
        for idx, i_object in enumerate(image_data['boxes']):
            cut_image = full_image[i_object['ymin']:i_object['ymax'], i_object['xmin']:i_object['xmax']]
            cut_object_name = "".join([os.path.splitext(image_data['img_name'])[0], '_',str(idx), ".jpg"])
            cut_object_path = os.path.join(self.dataset_classes_path_map[image_data['labels'][idx]], cut_object_name)
            width, height, depth = get_image_size(cut_image)
            if height>width:
                cut_image = ndimage.rotate(cut_image , 270)
            cv2.imwrite(cut_object_path, cut_image)
        return None

    def _cut_and_save_object_on_img(self, objects_on_images):
        """
        Method itare over images and run cuting method on them.
        :param objects_on_images: list of dict with images and metadata about them
        :type objects_on_images: list
        :retruns: None
        :rtype: None
        """
        for object_on_image in objects_on_images:
            self._cut_objects(image_data=object_on_image)
        return None

    def _resize_to_background_size(self, img):
        """
        Method resize background image.
        :param img: image
        :type img: numpy ndarray
        :retruns: image
        :rtype: numpy ndarray
        """
        return cv2.resize(img, (self.background_image_width, self.background_image_height))

    def _simple_paste_img_to_another(self, background_img, paste_img):
        """
        Method jast paste image in random place.
        :param background_img: image to paste on
        :type background_img: numpy ndarray
        :param paste_img: image to paste
        :type paste_img: numpy ndarray
        :retruns: background img
        :rtype: numpy ndarray
        """
        for i in range(100):
            try:
                # random cordynate of left uper edge of pasted img 
                left_x = random.randint(0, self.background_image_width)
                up_y = random.randint(0, self.background_image_height)
                background_img[up_y:up_y+paste_img.shape[0], left_x:left_x+paste_img.shape[1]] = paste_img
                return background_img
            except:
                pass
        raise ValueError("function: _simple_paste_img_to_another dont find place to paste img")

    def _simple_paste_nooverlaping_img_to_another(self, background_img, background_img_mask, paste_img):
        """
        Method paste image on image with no overlaping. 
        :param background_img: image to paste on
        :type background_img: numpy ndarray
        :param background_img_mask: mask of image to paste on
        :type background_img_mask: numpy ndarray
        :param paste_img: image to paste
        :type paste_img: numpy ndarray
        :retruns: background img
        :rtype: numpy ndarray
        """
        paste_img_box = {}
        for i in range(10):
            try:
                # random cordynate of left uper edge of pasted img 
                left_x = random.randint(0, self.background_image_width)
                up_y = random.randint(0, self.background_image_height)
                if not (background_img_mask[up_y:up_y+paste_img.shape[0], left_x:left_x+paste_img.shape[1]]==255).any():
                    paste_img_mask = 255 * np.ones(paste_img.shape, np.uint8)
                    background_img[up_y:up_y+paste_img.shape[0], left_x:left_x+paste_img.shape[1]] = paste_img
                    background_img_mask[up_y:up_y+paste_img.shape[0], left_x:left_x+paste_img.shape[1]] = paste_img_mask
                    paste_img_box = {
                        'xmin': left_x,
                        'ymin': up_y,
                        'xmax': left_x+paste_img.shape[1],
                        'ymax': up_y+paste_img.shape[0],
                    }
                    return background_img, background_img_mask, paste_img_box
            except ValueError:
                pass
            except:
                raise
        return background_img, background_img_mask, paste_img_box
       
    def _make_new_image(self, background_img_path, cut_image_list):
        """
        Method generate new image with bboxes by pasting cuted object 
        from images to new background in random places.
        :param background_img_path: image to paste on
        :type background_img_path: str
        :param cut_image_list: list of paths to images that can be paste on.
        :type cut_image_list: list
        :retruns: background image with pasted images
        :rtype: numpy ndarra
        :retruns: list of bboxes to that image
        :rtype: list
        """
        background_img = cv2.imread(background_img_path)
        background_img = self._background_image_transform(background_img)
        background_img = self._resize_to_background_size(background_img)
        background_img_mask = 0 * np.ones(background_img.shape, np.uint8)
        background_img_name = get_image_name(background_img_path)
        background_img_boxes = []

        for i in range(random.randint(self.min_cut_img_count, self.max_cut_img_count)):
            cut_image_path = random.choice(cut_image_list)
            cut_image_name = get_image_name(cut_image_path)
            cut_img = cv2.imread(cut_image_path)
            cut_img = self._cut_image_transform(cut_img)
            background_img, background_img_mask, paste_img_box = self._simple_paste_nooverlaping_img_to_another(background_img, background_img_mask, cut_img)
            if paste_img_box:
                background_img_boxes.append(paste_img_box)
        return background_img, background_img_boxes

    def _make_new_images_with_objects(self, image_limit_count, background_images_folder):
        """
        Method generate new image with bboxes by pasting cuted object 
        from images to new background in random places, and returning data in
        uniform data format. 
        :param image_limit_count: limit to full images (background with n small past images) we add
        :type image_limit_count: int
        :param background_images_folder: path to folder with background images
        :type background_images_folder: 
        :retruns: dict with 3 list : images, labels, list of dict of object data
        :rtype: dict
        """
        background_images = load_images(background_images_folder)
        output = {}
        images = []
        uniq_dataset_classes = []
        objects = []
        for class_name, class_folder_path in self.dataset_classes_path_map.items():
            cut_images = load_images(class_folder_path)
            if not cut_images:
                continue
            for i_img in range(image_limit_count):
                image_data = {}
                
                background_image_path = random.choice(background_images)
                background_img_name = get_image_name(background_image_path)
                file_name = '_'.join([class_name, background_img_name, str(i_img), '.jpg'])
                background_img, background_img_boxes = self._make_new_image(background_image_path, cut_images)
                file_path = os.path.join(self.tmp_folder, file_name)
                cv2.imwrite(file_path, background_img)
                images.append(file_path)
                image_data.update({'img_name': os.path.split(file_path)[1]})
                image_data.update({'img_path': file_path})
                image_data.update({'width': self.background_image_width})
                image_data.update({'height': self.background_image_height})
                image_data.update({'depth': self.background_image_depth})
                image_data.update({'boxes': background_img_boxes})
                image_data.update({'labels': [class_name for i in range(len(background_img_boxes))]})
                objects.append(image_data)
        output.update({'images': images})
        output.update({'dataset_classes': [class_name for class_name, class_folder_path in self.dataset_classes_path_map.items()]})
        output.update({'objects': objects})
        return output
        
    def _clean_tmp_structure(self):
        """
        Method that delate tmp folders after gen new data.
        """
        for class_name, class_folder in self.dataset_classes_map.items():
            remove_folder(class_folder)
        return None
            
    def _argument_data(self, data, base_path, dataset_name, image_limit_count, background_images_folder):
        """
        Mein method of this class. Method create folder structure make standart dataset with given data,
        then agument that dataset with artificail data nad deleta all tmp files.
        :param data: data in uniform format 
        :type data: dict
        :param base path where dataset will be save
        :type base_path: str
        :param dataset_name: dataset name
        :type dataset_name: str
        :param image_limit_count: limit to full images (background with n small past images) we add
        :type image_limit_count: int
        :param background_images_folder: path to folder with background images
        :type background_images_folder: 
        :retruns: dict with 3 list : images, labels, list of dict of object data
        :rtype: dict
        """
        self.make_dataset(data, base_path, dataset_name)
        self._create_tmp_structure()

        dataset_classes = data['dataset_classes']
        images_path = data['images']
        objects_on_images = data['objects']

        self._cut_and_save_object_on_img(objects_on_images)

        artificial_data = self._make_new_images_with_objects(image_limit_count, background_images_folder)
        self.make_dataset(artificial_data, base_path, dataset_name)
        self._clean_tmp_structure()
        return None

    def argument_data(self, data, base_path, dataset_name, image_limit_count, background_images_folder):
        """
        Abstract to mein method of this class. Method create folder structure make standart dataset with given data,
        then agument that dataset with artificail data nad deleta all tmp files.
        :param data: data in uniform format 
        :type data: dict
        :param base path where dataset will be save
        :type base_path: str
        :param dataset_name: dataset name
        :type dataset_name: str
        :param image_limit_count: limit to full images (background with n small past images) we add
        :type image_limit_count: int
        :param background_images_folder: path to folder with background images
        :type background_images_folder: 
        :retruns: dict with 3 list : images, labels, list of dict of object data
        :rtype: dict
        """
        return self._argument_data(data=data, base_path=base_path, dataset_name=dataset_name, 
                image_limit_count=image_limit_count, background_images_folder=background_images_folder)




