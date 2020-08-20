import os

from utils import load_images, load_text_paths, load_text_file_as_list, get_image_size
from exceptions import FoldersNamesError


class CocoDatasetReader(object):
    def __init__(self):
        super().__init__()
        self.dataset_path = ''
        self.image_extencion_format = '.jpg'
        self.images_folder_name = 'train_images'
        self.annotations_folder_name = 'train_labels'
        self.classes_names_filename = 'classes.names'
        self.images_folder_path = ''
        self.annotations_folder_path = ''
        self.class_names_file_path = ''

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
        self._save_to_instance_folder_paths(dataset_path)
        if os.path.exists(self.images_folder_path) and os.path.exists(self.annotations_folder_path):
            return True
        return False

    def _save_to_instance_folder_paths(self, dataset_path):
        """
        Method save paths to self.... in CocoDatasetReader.
        :param dataset_path: path to dataset folder
        :type dataset_path: str
        :return: None
        :rtype: None
        """
        self.dataset_path = dataset_path
        self.images_folder_path = os.path.join(dataset_path, self.images_folder_name)
        self.annotations_folder_path = os.path.join(dataset_path, self.annotations_folder_name)
        return None

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
        txts_paths = load_text_paths(self.annotations_folder_path)
        uniq_dataset_classes = []
        uniq_dataset_classes = self._load_dataset_classes_names()
        objects = []
        for text_path in txts_paths:
            text_object_dict, uniq_dataset_classes = self._read_text(text_path, uniq_dataset_classes)
            objects.append(text_object_dict)
        output_data_in_universa_od_format.update({'objects': objects})
        uniq_dataset_classes = self._format_dataset_classes(uniq_dataset_classes)
        output_data_in_universa_od_format.update({'dataset_classes': uniq_dataset_classes})
        return output_data_in_universa_od_format

    def _load_dataset_classes_names(self):
        self.class_names_file_path = os.path.join(self.dataset_path, self.classes_names_filename)
        return load_text_file_as_list(self.class_names_file_path)


    def _read_text(self, text_path, uniq_dataset_classes=[]):
        """
        Method that extract information from text file and return dict, 
        and update uniq dataset classes list.
        :param text_path: path to text file
        :type text_path: str
        :param uniq_dataset_classes: list of uniq class name
        :type uniq_dataset_classes: list
        :return: tuple with dict data from text and list of uniq class name
        :rtype: tuple
        """
        output_dict = {}
        image_filepath, image_filename = self._get_img_name_and_img_path_from_text_filename(text_path)
        output_dict['img_name'] = image_filename
        output_dict['img_path'] = image_filepath
        width, height, depth = get_image_size(output_dict['img_path'])
        output_dict['width'] = width
        output_dict['height'] = height
        output_dict['depth'] = depth
        labels = []
        boxes = []
        for label_bbox_str in load_text_file_as_list(text_path):
            bbox = {}
            label_bbox_list = label_bbox_str.split()
            labels.append(uniq_dataset_classes[int(label_bbox_list[0])])
            bbox['xmin'] = int(width * float(label_bbox_list[1]))
            bbox['ymax'] = int(height * float(label_bbox_list[2]))
            bbox['xmax'] = int((float(label_bbox_list[3]) * width) + bbox['xmin'])
            bbox['ymin'] = int((float(label_bbox_list[4]) * height) + bbox['ymax'])
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

    def _get_img_name_and_img_path_from_text_filename(self, text_path):
        """
        Method return imgname and imgpath form text_path.
        :param text_path: path to text file
        :type text_path: str
        :return: tuple with (image_filepath, image_filename)
        :rtype: tuple
        """
        _, text_filename = os.path.split(text_path)
        filename, _ =os.path.splitext(text_filename)
        image_filename = filename + self.image_extencion_format
        image_filepath = os.path.join(self.images_folder_path, image_filename)
        return image_filepath, image_filename
 





    