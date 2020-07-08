import os
import cv2
import random

from utils import load_images
from pascal_dataset_maker import PascalDatasetWriter

class PascalDataArgumenter(PascalDatasetWriter):
    def __init__(self):
        super().__init__()
        self.dataset_classes_path_map = dict()

    def create_tmp_structure(self):
        for key, value in self.dataset_classes_map.items():
            class_folder_path = os.path.join(self.dataset_folder_path, key)
            if not os.path.exists(class_folder_path):
                os.mkdir(class_folder_path)
            self.dataset_classes_path_map.update({key: class_folder_path})
        return None

    def cut_objects(self, image_data):
        full_image = cv2.imread(image_data['img_path'])
        for idx, i_object in enumerate(image_data['boxes']):
            cut_image = full_image[i_object['ymin']:i_object['ymax'],
                                    i_object['xmin']:i_object['xmax']]
            cut_object_name = "".join([os.path.splitext(image_data['img_name'])[0], '_',str(idx), ".jpg"])
            cut_object_path = os.path.join(self.dataset_classes_path_map[image_data['labels'][idx]], cut_object_name)
            cv2.imwrite(cut_object_path, cut_image)
        return None

    def cut_and_save_object(self, objects_on_images):
        for object_on_image in objects_on_images:
            self.cut_objects(image_data=object_on_image)

    def make_new_images_with_objects(self, image_limit_count, background_images_folder):
        background_images = load_images(background_images_folder)
        for class_name, class_folder_path in enumerate(self.dataset_classes_path_map):
            background_image = random.choice(background_images)
            cut_image = random.choice(class_folder_path)
            



            
    def argument_data(self, data, base_path, dataset_name, image_limit_count, background_images_folder):
        self.abstract_make_dataset(data, base_path, dataset_name)
        self.create_tmp_structure()

        dataset_classes = data['dataset_classes']
        images_path = data['images']
        objects_on_images = data['objects']

        self.cut_and_save_object(objects_on_images)

        self.make_new_images_with_objects(image_limit_count, background_images_folder)



        
    def abstract_argument_data(self, data, base_path, dataset_name):
        return self.argument_data(data, base_path, dataset_name)




