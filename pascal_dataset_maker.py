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
from xml.dom import minidom


class PascalDatasetWriter(object):
    """ Class build dolder structure and fill it with input data in pascal voc format.
    """
    def __init__(self):
        super().__init__()
        self.images_folder_name = 'JPEGImages'
        self.annotations_folder_name = 'Annotations'
        # place holder to store paths for later use
        self.dataset_name = ''
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
        self.dataset_name = dataset_name
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
        :retruns: new image path
        :rtype: str
        """
        _, image_name = os.path.split(old_image_path)
        new_image_path = os.path.join(self.images_folder_path, image_name)
        shutil.copyfile(old_image_path, new_image_path)
        return new_image_path

    def save_image_data_to_xml(self, image_data):
        """Method save data form dict ot xml files on drive.
        :param image_data: dict with inforamtion about image and all objce on that image.
        :type image_data: str
        :retruns: None
        :rtype: None
        """
        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "folder").text = self.dataset_name
        ET.SubElement(annotation, "filename").text = image_data['img_name']
        source = ET.SubElement(annotation, "source")
        ET.SubElement(source, "database").text='The dataset made uning universal object detection dataset maker'
        ET.SubElement(source, "info").text='The UODDM dataset type PASCAL VOC'
        size_field = ET.SubElement(annotation, "size")
        ET.SubElement(size_field, "width").text=str(image_data['width'])
        ET.SubElement(size_field, "height").text=str(image_data['height'])
        ET.SubElement(size_field, "depth").text=str(image_data['depth'])
        ET.SubElement(annotation, "segmented").text = '0'
        for idx, i_object in enumerate(image_data['boxes']):
            object = ET.SubElement(annotation, "object")
            ET.SubElement(object, "name").text=image_data['labels'][idx]
            ET.SubElement(object, "pose").text='Unspecified'
            ET.SubElement(object, "truncated").text='0'
            ET.SubElement(object, "difficult").text='0'
            bndbox = ET.SubElement(object, "bndbox")
            ET.SubElement(bndbox, "xmin").text=str(i_object['xmin'])
            ET.SubElement(bndbox, "ymin").text=str(i_object['ymin'])
            ET.SubElement(bndbox, "xmax").text=str(i_object['xmax'])
            ET.SubElement(bndbox, "ymax").text=str(i_object['ymax'])
        tree = ET.ElementTree(annotation)
        name_without_extention, extention = os.path.splitext(image_data['img_name'])
        file_path = os.path.join(self.annotations_folder_path, name_without_extention+".xml")
        tree.write(file_path, encoding='UTF-8')
        return None

    def save_images_and_labels(self, objects_on_images):
        """ Method iterate over list of dict with all imformation 
        about image and all objects on that image.
        :param objects_on_images: list of dict
        :type objects_on_images: list
        :retruns: None
        :rtype: None
        """
        for object_on_image in objects_on_images:
            # move image to new location, and rewrite img location in dict
            object_on_image['img_path'] = self.copy_image(object_on_image['img_path'])
            self.save_image_data_to_xml(object_on_image)
        return None
            
    def make_dataset(self, data, base_path, dataset_name):
        """ Method is main mathod of that class, method repaked the data and then
        make structure of dataset, then save all class names in dataset, and fill folders with
        images and data about object on that images.
        :param data: dict of data with images, labels, objects ... 
        :type data: dict
        :param base_path: base path where dataset will be save
        :type base_path: str
        :param base_path: dataset name and dataset folder name
        :type base_path: str
        :retruns: None
        :rtype: None
        """
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