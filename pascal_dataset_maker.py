"""The module builds dataset, folder structure and then repacks input data into
the appropriate folders. More info about format:
https://towardsdatascience.com/coco-data-format-for-object-detection-a4c5eaf518c5
In images_folder_name we save a images with id in name, annotations are save
in annotations_folder_name with id like image that they discrabe.
"""
# Right now no split to valid and train in folder structure.
import os
import xml.etree.ElementTree as ET

class PascalDatasetWriter(object):
    def __init__(self):
        super().__init__()
        self.images_folder_name = 'JPEGImages'
        self.annotations_folder_name = 'Annotations'
        # place holder to store paths for later use
        self.dataset_folder_path = ''
        self.images_folder_path = ''
        self.annotations_folder_path = ''

    def create_folder_structure(self, base_path, dataset_name):
        """Method create folder structure for dataset.
        :param base_path: base path where dataset will be make
        :type base_path: string
        :param dataset_name: dataset folder name
        :type dataset_name: string
        :retruns: None
        :rtype: None
        """
        self.dataset_folder_path = os.path.join(base_path, dataset_name)
        if not os.path.exists(self.dataset_folder_path):
            os.mkdir(self.dataset_folder_path)

        self.images_folder_path = os.path.join(self.dataset_folder_path, self.images_folder_name)
        if not os.path.exists(self.images_folder_path):
            os.mkdir(self.images_folder_path)

        self.annotations_folder_path = os.path.join(self.dataset_folder_path, self.annotations_folder_name)
        if not os.path.exists(self.annotations_folder_path):
            os.mkdir(self.annotations_folder_path)
        return None

    def make_dataset(self, data, base_path, dataset_name):
        self.create_folder_structure(base_path, dataset_name)

        
        
if __name__ == "__main__":
    kjn = PascalDatasetWriter()
    kjn.make_dataset(data='', base_path='', dataset_name='test')