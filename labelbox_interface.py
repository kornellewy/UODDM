""" Module is the interface between the json file from the label box portal and 
the universal objcet detection dataset maker internal modules.
"""
import os
import json
import urllib.request
import cv2
from scipy import ndimage

from utils import get_image_size

class LabelBoxInterface(object):
    """ Class that read json file form labelbox portal.
    :param tmp_folder: folder where temporarily store.
    :type tmp_folder: str
    """
    def __init__(self, tmp_folder='tmp'):
        super().__init__()
        self._check_and_create_tmp_folder(tmp_folder='tmp')
        self.tmp_folder = tmp_folder

    def _check_and_create_tmp_folder(self, tmp_folder='tmp'):
        if not os.path.exists(tmp_folder):
            os.mkdir(tmp_folder)
        return None
        
    def _check_images_orientation(self, image_path):
        """
        Check if dowloaded images have good orientation, and if bad
        orientation that will be rotated.
        :param image_path: path image
        :type image_path: str
        :retruns: None
        :rtype: None
        """
        width, height, depth = get_image_size(image_path)
        if height>width:
            image = cv2.imread(image_path)
            image = ndimage.rotate(image , 270)
            cv2.imwrite(image_path, image)
        return None

    def _get_data(self, json_file_path):
        """ Retrun dict with list of images and list of classes and list of objects,
        objects have img_path, widtha and height of image, list of dict with singel boxes,
        and list of labels.
        :param json_file_path: path to json file to open
        :type json_file_path: str
        :retruns: dict of json data
        :rtype: dict
        """
        output = {}
        objects = []
        images = []
        uniq_dataset_classes = []
        json_data = self._read_json_file(json_file_path)
        for image_json_object in json_data:
            if not bool(image_json_object["Label"]):
                continue
            object_data = {}
            image_save_path = os.path.join(self.tmp_folder, image_json_object["ID"]+".jpg")
            urllib.request.urlretrieve(image_json_object["Labeled Data"], image_save_path)
            self._check_images_orientation(image_save_path)
            boxes = list()
            labels = list()
            for object_on_img in image_json_object["Label"]["objects"]:
                xmin = object_on_img['bbox']['left']
                ymin = object_on_img['bbox']['top']
                xmax = xmin + object_on_img['bbox']['width']
                ymax = ymin + object_on_img['bbox']['height']
                boxes.append({'xmin':xmin, 'ymin':ymin, 'xmax':xmax, 'ymax':ymax})
                labels.append(object_on_img["value"])
                if not object_on_img["value"] in uniq_dataset_classes:
                    uniq_dataset_classes.append(object_on_img["value"])
            width, height, depth = get_image_size(image_save_path)
            object_data.update({'img_name': os.path.split(image_save_path)[1]})
            object_data.update({'img_path': image_save_path})
            object_data.update({'width': width})
            object_data.update({'height': height})
            object_data.update({'depth': depth})
            object_data.update({'boxes': boxes})
            object_data.update({'labels': labels})
            objects.append(object_data)
            images.append(image_save_path)
        output.update({'images': images})
        uniq_dataset_classes = self._format_dataset_classes(uniq_dataset_classes)
        output.update({'dataset_classes': uniq_dataset_classes})
        output.update({'objects': objects})
        return output

    def _read_json_file(self, json_file_path):
        """ Read json file form drive and return insides.
        :param json_file_path: path to json file to open
        :type json_file_path: str
        :retruns: dict of json data
        :rtype: dict
        """
        with open(json_file_path) as json_file:
            json_data = json.load(json_file)
        return json_data

    def _format_dataset_classes(self, dataset_classes):
        """ Reformat class names to have class 'background' on first place.
        :param dataset_classes: list of dataset classes
        :type dataset_classes: list
        :retruns: formated list of dataset classes 
        :rtype: list
        """
        # check if list have class 'background'
        if 'background' in dataset_classes:
            # check if 'background' on 1 first place in list
            if dataset_classes[0] == 'background':
                return dataset_classes
            else:
                dataset_classes.remove('background')
                dataset_classes = ['background'] + dataset_classes
                return dataset_classes
        else:
            dataset_classes = ['background'] + dataset_classes
            return dataset_classes

    def get_data(self, json_file_path):
        """ Abstract interface to call main method of that class.
        That main metod of class, u need only to call thet method.
        :param json_file_path: path to json file to open
        :type json_file_path: str
        :retruns: dict of json data
        :rtype: dict
        """
        return self._get_data(json_file_path)
    
if __name__ == "__main__":
    TEST_FILE = 'test_files/test_dataset.json'
    TMP_FOLDER = 'tmp'
    kjn = LabelBoxInterface()
    print(kjn._get_data(TEST_FILE))


