import os
import xml.etree.ElementTree as ET

from utils import load_xml_paths, load_images
from exceptions import FoldersNamesError

class PascalDatasetReader(object):
    """
    Class that read pascal dataset format to universal OD format. 
    If u have images and annotation in difrent names space than
    define use method: .change_folder_to_find_names
    """
    def __init__(self):
        super().__init__()
        self.dataset_path = ''
        self.images_folder_name = 'JPEGImages'
        self.annotations_folder_name = 'Annotations'
        self.images_folder_path = ''
        self.annotations_folder_path = ''

    def change_folder_to_find_names(self, images_folder_name, annotations_folder_name):
        """
        Method that change folder names to find.
        :param images_folder_name: image folder in datataset
        :type images_folder_name: str
        :param annotations_folder_name: annotaion foldet in dataset
        :type annotations_folder_name: str
        :return: None
        :rtype: None
        """
        self.images_folder_name = images_folder_name
        self.annotations_folder_name = annotations_folder_name
        return None

    def get_data(self, dataset_path):
        """
        Mein method of this class, it return data form given dataset path in
        universal OD format.
        :param dataset_path: path to dataset folder
        :type dataset_path: str
        :return: dict in universal object detection format
        :rtype: dict
        """
        return self._get_data(dataset_path)  

    def _get_data(self, dataset_path):
        """
        Method check if dataset have good folders names.
        Then run extracion function from folders and return data in universal OD format.
        :param dataset_path: path to dataset folder
        :type dataset_path: str
        :return: dict in universal object detection format
        :rtype: dict
        """
        output_data_in_universa_od_format = ''
        if self._test_structure_exist(dataset_path):
            output_data_in_universa_od_format = self._extract_data_from_folders()
        else:
            raise FoldersNamesError(self.images_folder_name, self.annotations_folder_name)
        return output_data_in_universa_od_format

    def _test_structure_exist(self, dataset_path):
        """
        Method defina dataset paths and check if folder structure 
        have good names and them exist. 
        :param dataset_path: path to dataset folder
        :type dataset_path: str
        :return: if folders exist true ales false
        :rtype: bool
        """
        self.dataset_path = dataset_path
        self.images_folder_path = os.path.join(dataset_path, self.images_folder_name)
        self.annotations_folder_path = os.path.join(dataset_path, self.annotations_folder_name)
        if os.path.exists(self.images_folder_path) and os.path.exists(self.annotations_folder_path):
            return True
        return False

    def _extract_data_from_folders(self):
        """
        Method that extract data form annotraion and images folder.
        :return: dict in universal object detection format
        :rtype: dict
        """
        output_data_in_universa_od_format = {}
        output_data_in_universa_od_format = self._extract_data_from_image_folder(output_data_in_universa_od_format) 
        output_data_in_universa_od_format = self._extract_data_from_annotations_folder(output_data_in_universa_od_format)
        return output_data_in_universa_od_format

    def _extract_data_from_image_folder(self, output_data_in_universa_od_format):
        """
        Method that extract data form images folder.
        :param output_data_in_universa_od_format: dict in universal object detection format without images
        :type output_data_in_universa_od_format: dict
        :return: dict in universal object detection format with images
        :rtype: dict
        """
        output_data_in_universa_od_format.update({'images': load_images(self.images_folder_path)}) 
        return output_data_in_universa_od_format

    def _extract_data_from_annotations_folder(self, output_data_in_universa_od_format):
        """
        Method that extract data form annotations folder.
        :param output_data_in_universa_od_format: dict in universal object detection format without annotations
        :type output_data_in_universa_od_format: dict
        :return: dict in universal object detection format with annotations
        :rtype: dict
        """
        xmls = load_xml_paths(self.annotations_folder_path)
        uniq_dataset_classes = []
        objects = []
        for xml_file_path in xmls:
            xml_object_dict, uniq_dataset_classes = self._read_xml(xml_file_path, uniq_dataset_classes)
            objects.append(xml_object_dict)
        output_data_in_universa_od_format.update({'objects': objects})
        uniq_dataset_classes = self._format_dataset_classes(uniq_dataset_classes)
        output_data_in_universa_od_format.update({'dataset_classes': uniq_dataset_classes})
        return output_data_in_universa_od_format

    def _read_xml(self, xml_path, uniq_dataset_classes=[]):
        """
        Method that extract information from xml file and return dict, 
        and update uniq dataset classes list.
        :param xml_path: path to xml file
        :type xml_path: str
        :param uniq_dataset_classes: list of uniq class name
        :type uniq_dataset_classes: lsit
        :return: tuple with dict data from xml and list of uniq class name
        :rtype: tuple
        """
        output_dict = {}
        annotation = ET.parse(xml_path).getroot()
        output_dict['img_name'] = annotation.find('filename').text
        output_dict['img_path'] = os.path.join(self.images_folder_path, annotation.find('filename').text)
        output_dict['width'] = annotation.find('size').find('width').text
        output_dict['height'] = annotation.find('size').find('height').text
        output_dict['depth'] = annotation.find('size').find('depth').text
        labels = []
        boxes = []
        for i_object in annotation.findall('object'):
            bbox = {}
            bbox['xmin'] = i_object.find('bndbox').find('xmin')
            bbox['ymin'] = i_object.find('bndbox').find('ymin')
            bbox['xmax'] = i_object.find('bndbox').find('xmax')
            bbox['ymax'] = i_object.find('bndbox').find('ymax')
            class_name = i_object.find('name').text
            if class_name not in uniq_dataset_classes:
                uniq_dataset_classes.append(class_name)
            labels.append(i_object.find('name').text)
            boxes.append(bbox)
        output_dict['boxes'] = boxes
        output_dict['labels'] = labels
        return output_dict, uniq_dataset_classes

    def _format_dataset_classes(self, dataset_classes):
        """ 
        Reformat class names to have class 'background' on first place.
        :param dataset_classes: list of dataset classes
        :type dataset_classes: list
        :retruns: formated list of dataset classes 
        :rtype: list
        """
        if 'background' in dataset_classes:
            if dataset_classes[0] == 'background':
                return dataset_classes
            else:
                dataset_classes.remove('background')
                dataset_classes = ['background'] + dataset_classes
                return dataset_classes
        else:
            dataset_classes = ['background'] + dataset_classes
            return dataset_classes
