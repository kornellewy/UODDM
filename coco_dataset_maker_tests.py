import os 
import unittest

from coco_dataset_maker import CocoDatasetWriter
from labelbox_interface import LabelBoxInterface
from utils import load_images, remove_folder, find_all_dirs_names, \
                    find_all_jpg, clean_tmp, load_images_names, load_text_files

class ClassificationDatasetMakerTests(unittest.TestCase):
    def setUp(self):
        self.tmp_path = 'tmp'
        self.output_path = ''
        self.dataset_name = 'test_coco_dataset'
        self.images_folder_name = 'train_images'
        self.annotations_folder_name = 'train_labels'
        self.classes_names_filename = 'classes.names'
        self.dataset_path = os.path.join(self.output_path, self.dataset_name)
        self.images_path = os.path.join(self.dataset_name, self.images_folder_name)
        self.annotations_path = os.path.join(self.dataset_name, self.annotations_folder_name)
        self.classes_names_path = os.path.join(self.dataset_path, self.classes_names_filename)
        # get test data
        self.labelbox_json_path = 'test_files/test_dataset.json'
        self.labelbox_interface = LabelBoxInterface()
        self.test_lablebox_data = self.labelbox_interface.get_data(self.labelbox_json_path)
        # init class writer
        self.datasetmaker = CocoDatasetWriter()
        self.datasetmaker.make_dataset(self.test_lablebox_data, '', self.dataset_name)

    def test_tmp_exist(self):
        self.assertEqual(os.path.exists(self.tmp_path), True)

    def test_create_dataset_folder(self):
        self.assertEqual(os.path.exists(self.dataset_path), True)

    def test_create_images_folder(self):
        self.assertEqual(os.path.exists(self.images_path), True)

    def test_create_annotations_folder(self):
        self.assertEqual(os.path.exists(self.annotations_path), True)

    def test_create_classes_names_file(self):
        self.assertEqual(os.path.exists(self.classes_names_path), True)

    def test_any_image_in_images_folder_in_dataset(self):
        self.assertEqual(len(load_images(self.images_path)) == 0, False)

    def test_txt_file_to_image(self):
        images = load_images_names(self.images_path)
        folder_txts = load_text_files(self.annotations_path)
        folder_txts.sort()
        txts_form_images_names = []
        for image in images:
            label_txt_filename = image + '.txt'
            label_txt_filepath = os.path.join(self.annotations_path, label_txt_filename)
            txts_form_images_names.append(label_txt_filepath)
        txts_form_images_names.sort()
        self.assertEqual(txts_form_images_names == folder_txts, True)        

    def tearDown(self): 
        remove_folder(self.dataset_name)
        clean_tmp(self.tmp_path)

if __name__ == '__main__':
    unittest.main()