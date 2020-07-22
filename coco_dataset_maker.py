"""
The module builds dataset, folder structure and then repacks input data into
the appropriate folders. More info about format:
https://towardsdatascience.com/coco-data-format-for-object-detection-a4c5eaf518c5
COCO Bounding box: (x-top left, y-top left, width, height)
Pascal VOC Bounding box :
(x-top left, y-top left,x-bottom right, y-bottom right)
"""
import os
import shutil

# TODO: format is 2014 check if 2017 changemin some way
class CocoDatasetWriter(object):
    def __init__(self):
        super().__init__()
        self.images_folder_name = 'train_images'
        self.annotations_folder_name = 'train_labels'
        self.classes_names_filename = 'classes.names'
        self.dataset_name = ''
        self.dataset_folder_path = ''
        self.images_folder_path = ''
        self.annotations_folder_path = ''
        self.classes_names_path = ''
        self.dataset_classes_to_idx_map = dict()

    def make_dataset(self, data, base_path, dataset_name):
        """ 
        Method is main mathod of that class, method repaked the data and then
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
        return self._make_dataset(data, base_path, dataset_name)

    def _make_dataset(self, data, base_path, dataset_name):
        """ 
        Method is main mathod of that class, method repaked the data and then
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
        self._create_folder_structure(base_path, dataset_name)
        self._create_classes_names(dataset_classes)
        self._create_classes_to_idx_map(dataset_classes)
        self._save_images_and_labels(objects_on_images)
        return None

    def _create_folder_structure(self, base_path, dataset_name):
        """
        Method create folder structure for dataset.
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
    
    def _create_classes_names(self, dataset_classes):
        """
        Method classes.names create file that have classes names. 
        :param dataset_classes: list of classes names
        :type dataset_classes: list
        :retruns: None
        :rtype: None
        """
        self.classes_names_path = os.path.join(self.dataset_folder_path, self.classes_names_filename)
        with open(self.classes_names_path, 'a+') as f:
            for classs in dataset_classes:
                f.write(str(classs)+'\n')
        return None
        
    def _create_classes_to_idx_map(self, dataset_classes):
        """
        Method create dict of dataset_classes, where key is a dataset class
        and value is index.
        :param dataset_classes: list of classes names
        :type dataset_classes: list
        :retruns: None
        :rtype: None
        """
        # credit: https://stackoverflow.com/questions/36459969/python-convert-list-to-dictionary-with-indexess
        self.dataset_classes_to_idx_map = {k: v for v, k in enumerate(dataset_classes)}
        return None

    def _save_images_and_labels(self, objects_on_images):
        for image_object in objects_on_images:
            image_object['img_path'] = self._copy_image(image_object['img_path'])
            self._make_annotations_file(image_object)
        return None

    def _copy_image(self, old_image_path):
        """
        Method copy image from old folder location to new folder.
        :param old_image_path: image save path, place where images 
                                is save before run of function.
        :type old_image_path: str
        :retruns: new image path
        :rtype: str
        """
        _, image_name = os.path.split(old_image_path)
        new_image_path = os.path.join(self.images_folder_path, image_name)
        shutil.copyfile(old_image_path, new_image_path)
        return new_image_path   
        
    def _make_annotations_file(self, image_object):
        """
        Method generate name for txt file with labels and 
        start method that save data to that file.
        :param image_object: dict of all info about img and object on it
        :type image_object: dict
        :retruns: none
        :rtype: none
        """
        annotations_file_name =  self._return_annotations_file_name(image_object['img_path'])
        annotations_file_path = os.path.join(self.annotations_folder_path, annotations_file_name)
        self._save_txt_file(image_object, annotations_file_path)
        return None

    def _return_annotations_file_name(self, img_path):
        """
        Method generate label txt filename from img name.
        :param img_path: path to img
        :type image_object: str
        :retruns: filename for txt file with labels
        :rtype: str
        """
        img_name = img_path
        _, img_name = os.path.split(img_name)
        return os.path.splitext(img_name)[0] + '.txt'

    def _save_txt_file(self, image_object, annotations_file_path):
        """
        Method extract data from dict and repack them to coco format and save in txt.
        :param image_object: dict of data about all bbox on img
        :type image_object: dict
        :param annotations_file_path: path to txt file with labels
        :type annotations_file_path: str
        :retruns: None
        :rtype: None
        """
        # example COCO Bounding box: (x-top left, y-top left, width, height)
        # 49 0.646836 0.132552 0.118047 0.096937
        img_height = image_object['height']
        img_width = image_object['width']
        rows_of_label_and_bbox = []
        for label, bbox in zip(image_object['labels'], image_object['boxes']):
            row_to_write = ''
            class_idx = str(self.dataset_classes_to_idx_map[label])
            bbox_x_top_left = str(round(bbox['xmin']/img_width, 6))
            bbox_y_top_left = str(round(bbox['ymax']/img_height, 6))
            bbox_width = str(round((bbox['xmax']-bbox['xmin'])/img_width, 6))
            bbox_height = str(round((bbox['ymax']-bbox['ymin'])/img_height, 6))
            row_to_write = ' '.join([class_idx, bbox_x_top_left,
                                 bbox_y_top_left, bbox_width, bbox_height])
            rows_of_label_and_bbox.append(row_to_write)
        self._save_file(rows_of_label_and_bbox, annotations_file_path)
        return None

    def _save_file(self, list_of_classes_and_bbox, filepath):
        """
        Method save list of strings with data about bbox in filepath.
        :param list_of_classes_and_bbox: list of bbox with lables
        :type list_of_classes_and_bbox: list
        :param filepath: path to txt file 
        :type filepath: str
        """
        with open(filepath, 'a+') as file:
            for r in list_of_classes_and_bbox:
                file.write(r + '\n')
        return None
