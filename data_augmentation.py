#TODO: komentarze
import os
import cv2
import random
import numpy as np
from scipy import ndimage
import math
from PIL import Image


from utils import load_images, load_images_names
from pascal_dataset_maker import PascalDatasetWriter
from data_argumentation_utils import DataRandomModifier


class PascalDataArgumenter(PascalDatasetWriter):
    def __init__(self, tmp_folder='tmp'):
        super().__init__()
        self.dataset_classes_path_map = dict()
        self.image_random_modifier = DataRandomModifier()
        self.tmp_folder = tmp_folder
        #TODO: komentarze
        self.min_cut_img_count = 1
        self.max_cut_img_count = 5
        self.background_image_width = 1920
        self.background_image_height = 1080
        self.background_image_depth = 3
        self.transforms_probability = 0.5

    def background_image_transform(self, image):
        #TODO: komentarze
        image = self.image_random_modifier.random_crop(image)
        image = self.image_random_modifier.random_horizontal_filp(image)
        image = self.image_random_modifier.random_vertical_filp(image)
        image = self.image_random_modifier.random_channel_swap(image)
        image = self.image_random_modifier.random_blur(image, 0.3)
        image = self.image_random_modifier.random_gaussian_noise(image, 0.1)
        image = self.image_random_modifier.random_img_to_gray(image, 0.1)
        return image

    def cut_image_transform(self, image):
        #TODO: komentarze
        image = self.image_random_modifier.random_channel_swap(image)
        image = self.image_random_modifier.random_blur(image, 0.3)
        image = self.image_random_modifier.random_gaussian_noise(image, 0.1)
        image = self.image_random_modifier.random_img_to_gray(image, 0.1)
        return image

    def create_tmp_structure(self):
        #TODO: komentarze
        for key, value in self.dataset_classes_map.items():
            class_folder_path = os.path.join(self.dataset_folder_path, key)
            if not os.path.exists(class_folder_path):
                os.mkdir(class_folder_path)
            self.dataset_classes_path_map.update({key: class_folder_path})
        return None

    def get_image_name(self, path):
        #TODO: komentarze
        _, name = os.path.split(path)
        name, _ = os.path.splitext(name)
        return name

    def get_image_size(self, img):
        """ Return width, height of image.
        :param img_path: path to image on dirve
        :type img_path: str
        :retruns: width, height of img
        :rtype: tuple
        """
        if isinstance(img, str):
            img = cv2.imread(img)
        elif isinstance(img, np.ndarray):
            pass
        height, width, depth = img.shape
        return width, height, depth

    def cut_objects(self, image_data):
        #TODO: komentarze
        full_image = cv2.imread(image_data['img_path'])
        width, height, depth = self. get_image_size(full_image)
        if height>width:
            full_image = ndimage.rotate(full_image , 90)
        for idx, i_object in enumerate(image_data['boxes']):
            cut_image = full_image[i_object['ymin']:i_object['ymax'], i_object['xmin']:i_object['xmax']]
            cut_object_name = "".join([os.path.splitext(image_data['img_name'])[0], '_',str(idx), ".jpg"])
            cut_object_path = os.path.join(self.dataset_classes_path_map[image_data['labels'][idx]], cut_object_name)
            width, height, depth = self. get_image_size(cut_image)
            if height>width:
                cut_image = ndimage.rotate(cut_image , 270)
            cv2.imwrite(cut_object_path, cut_image)
        return None

    def cut_and_save_object(self, objects_on_images):
        #TODO: komentarze
        for object_on_image in objects_on_images:
            self.cut_objects(image_data=object_on_image)

    def _resize_to_background_size(self, img):
        #TODO: komentarze
        return cv2.resize(img, (self.background_image_width, self.background_image_height))



    def _simple_paste_img_to_another(self, background_img, paste_img):
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
       

    def make_new_image(self, background_img_path, cut_image_list):
        #TODO: komentarze
        
        background_img = cv2.imread(background_img_path)
        background_img = self.background_image_transform(background_img)
        background_img = self._resize_to_background_size(background_img)
        background_img_mask = 0 * np.ones(background_img.shape, np.uint8)
        background_img_name = self.get_image_name(background_img_path)
        background_img_boxes = []

        for i in range(random.randint(self.min_cut_img_count, self.max_cut_img_count)):
            cut_image_path = random.choice(cut_image_list)
            cut_image_name = self.get_image_name(cut_image_path)
            cut_img = cv2.imread(cut_image_path)
            cut_img = self.cut_image_transform(cut_img)
            background_img, background_img_mask, paste_img_box = self._simple_paste_nooverlaping_img_to_another(background_img, background_img_mask, cut_img)
            if paste_img_box:
                background_img_boxes.append(paste_img_box)
        return background_img, background_img_boxes


    def make_new_images_with_objects(self, image_limit_count, background_images_folder):
        #TODO: komentarze
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
                background_img_name = self.get_image_name(background_image_path)
                file_name = '_'.join([class_name, background_img_name, str(i_img), '.jpg'])
                background_img, background_img_boxes = self.make_new_image(background_image_path, cut_images)
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
        

    def argument_data(self, data, base_path, dataset_name, image_limit_count, background_images_folder):
        #TODO: komentarze
        self.abstract_make_dataset(data, base_path, dataset_name)
        self.create_tmp_structure()

        dataset_classes = data['dataset_classes']
        images_path = data['images']
        objects_on_images = data['objects']

        self.cut_and_save_object(objects_on_images)

        artificial_data = self.make_new_images_with_objects(image_limit_count, background_images_folder)
        self.abstract_make_dataset(artificial_data, base_path, dataset_name)

    def abstract_argument_data(self, data, base_path, dataset_name, image_limit_count, background_images_folder):
        return self.argument_data(data=data, base_path=base_path, dataset_name=dataset_name, 
                image_limit_count=image_limit_count, background_images_folder=background_images_folder)




