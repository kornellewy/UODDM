"""The module builds dataset, folder structure and then repacks input data into
the appropriate folders. More info about format:
https://towardsdatascience.com/coco-data-format-for-object-detection-a4c5eaf518c5
In images_folder_name we save a images with id in name, annotations are save
in annotations_folder_name with id like image that they discrabe.
"""
# Right now no split to valid and train in folder structure.
import os
import shutil
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
        self.dataset_classes_map = dict()

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

    def create_classes_names(self, dataset_classes):
        """Method classes.names create file that have classes names. 
        :param dataset_classes: list of classes names
        :type dataset_classes: list
        :retruns: None
        :rtype: None
        """
        class_names_file_path = os.path.join(self.dataset_folder_path, 'classes.names')
        with open(class_names_file_path, 'a+') as f:
            for classs in dataset_classes:
                f.write(str(classs)+'\n')
        return None

    def create_classes_map(self, dataset_classes):
        """Method create dict of dataset_classes, where key is a dataset class and value is index.
        :param dataset_classes: list of classes names
        :type dataset_classes: list
        :retruns: None
        :rtype: None
        """
        # credit: https://stackoverflow.com/questions/36459969/python-convert-list-to-dictionary-with-indexess
        self.dataset_classes_map = {k: v for v, k in enumerate(dataset_classes)}
        return None

    def copy_image(self, old_image_path):
        """Method copy image from old folder location to new folder.
        :param old_image_path: image save path, place where images is save before run of function.
        :type old_image_path: str
        :retruns: None
        :rtype: None
        """
        _, image_name = os.path.split(old_image_path)
        new_image_path = os.path.join(self.images_folder_name, image_name)
        shutil.copyfile(old_image_path, new_image_path)
        return None

    def save_images_and_labels(self, objects_on_images):
        # del
        import pprint
        for object_on_image in objects_on_images:
            pprint.pprint(object_on_image)


    def make_dataset(self, data, base_path, dataset_name):
        dataset_classes = data['dataset_classes']
        images_path = data['images']
        objects_on_images = data['objects']

        self.create_folder_structure(base_path, dataset_name)
        self.create_classes_names(dataset_classes)
        self.create_classes_map(dataset_classes)
        self.save_images_and_labels(objects_on_images)





        
        
if __name__ == "__main__":
    kjn = PascalDatasetWriter()
    kjn.make_dataset(data='', base_path='', dataset_name='test')