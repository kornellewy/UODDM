import os 
import unittest

from clasification_dataset_maker import ClassificationDatasetMaker
from labelbox_interface import LabelBoxInterface
from utils import load_images, remove_folder, find_all_dirs_names, find_all_jpg, clean_tmp


class ClassificationDatasetMakerTests(unittest.TestCase):
    def setUp(self):
        self.tmp_path = 'tmp'
        self.output_path = ''
        self.dataset_name = 'test_classification_dataset'
        self.dataset_path = os.path.join(self.output_path, self.dataset_name)
        self.labelbox_json_path = 'test_files/test_dataset.json'
        self.labelbox_interface = LabelBoxInterface()
        self.test_lablebox_data = self.labelbox_interface.get_data(self.labelbox_json_path)\
        
        dataset_maker = ClassificationDatasetMaker(tmp_folder=self.tmp_path)
        user_class_to_folder_map = {
            'pricetag': 'test_classification_dataset/background',
            'backgroud': 'test_classification_dataset/background',
            'background': 'test_classification_dataset/background'
        }
        dataset_maker.make_dataset(output_path = self.output_path, dataset_name=self.dataset_name, 
        universal_OD_data=self.test_lablebox_data, user_class_to_folder_map=user_class_to_folder_map)

    def test_tmp_exist(self):
        self.assertEqual(os.path.exists(self.tmp_path), True)

    # def test_tmp_clean(self):
    #     dataset_maker = ClassificationDatasetMaker(tmp_folder=self.tmp_path)
    #     self.assertEqual(len(load_images(self.tmp_path)), 0)

    def test_create_dataset_folder(self):
        self.assertEqual(os.path.exists(self.dataset_path), True)

    def test_create_dataset_classes_folders(self):
        self.assertEqual(find_all_dirs_names(self.dataset_path).sort(), self.test_lablebox_data['dataset_classes'].sort())

    def test_cut_and_save_images(self):
        self.assertEqual(len(find_all_jpg(self.dataset_path))>0, True)

    def test_user_maping(self):
        self.assertEqual(len(find_all_jpg('test_classification_dataset/pricetag'))==0, True)
        self.assertEqual(len(find_all_jpg('test_classification_dataset/backgroud'))==0, True)


    def tearDown(self): 
        remove_folder(self.dataset_name)
        clean_tmp(self.tmp_path)

    
         
if __name__ == '__main__':
    unittest.main()