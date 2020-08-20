import os 
import unittest

from labelbox_interface import LabelBoxInterface
from coco_dataset_maker import CocoDatasetWriter
from coco_dataset_interface import CocoDatasetReader
from exceptions import FoldersNamesError
from utils import load_text_paths, load_images, remove_folder

class CocoDatasetReaderTests(unittest.TestCase):
    def setUp(self):
        self.dataset_name = 'Coco_dataset_reader_test'
        self.labelbox_json_path = 'test_files/test_dataset.json'
        self.labelbox_interface = LabelBoxInterface()
        self.test_lablebox_data = self.labelbox_interface.get_data(self.labelbox_json_path)
        self.datasetmaker = CocoDatasetWriter()
        self.datasetmaker.make_dataset(self.test_lablebox_data, '', self.dataset_name)

    def test_changing_folder_names_to_find(self):
        images_folder_name = 'test_changing_folder_names_to_find'
        annotations_folder_name = 'test_changing_folder_names_to_find'
        coco_reader = CocoDatasetReader()
        coco_reader.change_folder_to_find_names(images_folder_name=images_folder_name, annotations_folder_name=annotations_folder_name)
        self.assertEqual(coco_reader.images_folder_name, images_folder_name)
        self.assertEqual(coco_reader.annotations_folder_name, annotations_folder_name)

    def test_FoldersNamesError_raise(self):
        dataset_path = 'test_files'
        coco_reader = CocoDatasetReader()
        self.assertRaises(FoldersNamesError, coco_reader.get_data, dataset_path)

    def test_text_paths_loading(self):
        coco_reader = CocoDatasetReader()
        coco_reader._test_structure_exist(self.dataset_name)
        texts = load_text_paths(coco_reader.annotations_folder_path)
        self.assertEqual(len(texts)>0, True)

    def test_extract_data_from_image_folder(self):
        test_data = {}
        coco_reader = CocoDatasetReader()
        coco_reader._test_structure_exist(self.dataset_name)
        test_data = coco_reader._extract_data_from_image_folder(test_data)
        self.assertEqual(isinstance(test_data['images'], list) , True)
        self.assertEqual(len(test_data['images']) > 0, True)

    def test_get_img_name_and_img_path_from_text_filename(self):
        coco_reader = CocoDatasetReader()
        labels_folder_path = os.path.join(self.dataset_name, 'train_labels')
        images_folder_path = os.path.join(self.dataset_name, 'train_images')
        text_path = load_text_paths(labels_folder_path)[0]
        coco_reader._save_to_instance_folder_paths(self.dataset_name)
        image_filepath, image_filename = coco_reader._get_img_name_and_img_path_from_text_filename(text_path)
        self.assertEqual(image_filepath in load_images(images_folder_path), True)

    def test_read_text(self):
        coco_reader = CocoDatasetReader()
        labels_folder_path = os.path.join(self.dataset_name, 'train_labels')
        images_folder_path = os.path.join(self.dataset_name, 'train_images')
        text_path = load_text_paths(labels_folder_path)[0]
        coco_reader._save_to_instance_folder_paths(self.dataset_name)
        data_in_output_format, _ = coco_reader._read_text(text_path, ["test", "test"])
        self.assertEqual(len(data_in_output_format['boxes'])>0, True)
        self.assertEqual(len(data_in_output_format['labels'])>0, True)
        self.assertEqual(len(data_in_output_format['boxes']), len(data_in_output_format['labels']))

    def test_if_output_data_have_objects(self):
        coco_reader = CocoDatasetReader()
        data_in_output_format = coco_reader.get_data(self.dataset_name)
        self.assertEqual(len(data_in_output_format['objects'])>0, True)

    def test_if_output_data_have_images(self):
        coco_reader = CocoDatasetReader()
        data_in_output_format = coco_reader.get_data(self.dataset_name)
        self.assertEqual(len(data_in_output_format['dataset_classes'])>0, True)

    def tearDown(self):
        remove_folder(self.dataset_name)

if __name__ == '__main__':
    unittest.main()