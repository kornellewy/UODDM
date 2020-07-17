import os
import cv2

from utils import clean_tmp 

class ClassificationDatasetMaker(object):
    def __init__(self, tmp_folder='tmp'):
        super().__init__()
        self.tmp_folder = 'tmp'
        # uncoment when not debuging
        # clean_tmp(self.tmp_folder)
        self.dataset_path = ''
        self.class_to_path_map = {}

    def make_dataset(self, output_path, dataset_name, universal_OD_data, user_class_to_folder_map = None):
        self._create_structure_of_dataset(output_path=output_path, dataset_name=dataset_name,
        classes_names=universal_OD_data['dataset_classes'])
        if user_class_to_folder_map is not None:
            self.class_to_path_map = user_class_to_folder_map
        self._cut_save_images_in_proper_classfolders(universal_OD_data)
        return None

    def _create_structure_of_dataset(self, output_path, dataset_name, classes_names):
        """
        Method create folder structure of dataset, so main folder named dataset_namem,
        and inside it subfolders named after names in classes_names
        :param output_path: path where to create dataset 
        :type output_path: str
        :param dataset_name: dataset name for folder
        :type dataset_name: str
        :param classes_names: list of classes in dataset, that will be use to create subfolders
        named after elements in that list
        :type classes_names: list
        :returns: None
        :rtype: None
        """
        self.dataset_path = os.path.join(output_path, dataset_name)
        if not os.path.exists(self.dataset_path):
            os.mkdir(self.dataset_path)
            for class_name in classes_names:
                class_path = os.path.join(self.dataset_path, class_name)
                self.class_to_path_map.update({class_name: class_path})
                if not os.path.exists(class_path):
                    os.mkdir(class_path)
        else:
            for class_name in classes_names:
                class_path = os.path.join(self.dataset_path, class_name)
                self.class_to_path_map.update({class_name: class_path})
                if not os.path.exists(class_path):
                    os.mkdir(class_path)
        return None

    def _cut_save_images_in_proper_classfolders(self, universal_OD_data):
        """
        Method iterate over object in universal_OD_data and
        cut images form objects list. Then save cut images to proper 
        class folders. 
        :param universal_OD_data: OD dataset in universal format
        :type universal_OD_data: dict
        :returns: None
        :rtype: None
        """
        for img_idx, img_metadata in enumerate(universal_OD_data['objects']):
            full_original_image = cv2.imread(img_metadata['img_path'])
            for object_idx, object_data in enumerate(img_metadata['boxes']):
                cut_image = full_original_image[object_data['ymin']:object_data['ymax'], object_data['xmin']:object_data['xmax']]
                cut_img_path = os.path.join(self.class_to_path_map[img_metadata['labels'][object_idx]], str(img_idx)+'_'+ str(object_idx)+ ".jpg")
                cv2.imwrite(cut_img_path, cut_image)
        return None


