import os 
import unittest

from coco_dataset_interface import CocoDatasetReader
from coco_dataset_maker import CocoDatasetWriter
from pascal_dataset_interface import PascalDatasetReader
from pascal_dataset_maker import PascalDatasetWriter
from clasification_dataset_maker import ClassificationDatasetMaker
from labelbox_interface import LabelBoxInterface
from utils import load_images, remove_folder, find_all_dirs_names, find_all_jpg,\
                     clean_tmp, load_xml_paths, load_text_paths, load_images_names
from exceptions import FoldersNamesError

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


class PascalDatasetReaderTests(unittest.TestCase):
    def setUp(self):
        self.dataset_name = 'pascal_dataset_reader_test'
        self.labelbox_json_path = 'test_files/test_dataset.json'
        self.labelbox_interface = LabelBoxInterface()
        self.test_lablebox_data = self.labelbox_interface.get_data(self.labelbox_json_path)
        # init class writer
        self.datasetmaker = PascalDatasetWriter()
        self.datasetmaker.make_dataset(self.test_lablebox_data, '', self.dataset_name)
        
    def test_changing_folder_names_to_find(self):
        images_folder_name = 'test_changing_folder_names_to_find'
        annotations_folder_name = 'test_changing_folder_names_to_find'
        pascal_reader = PascalDatasetReader()
        pascal_reader.change_folder_to_find_names(images_folder_name=images_folder_name, annotations_folder_name=annotations_folder_name)
        self.assertEqual(pascal_reader.images_folder_name, images_folder_name)
        self.assertEqual(pascal_reader.annotations_folder_name, annotations_folder_name)

    def test_PascalFoldersNamesError_raise(self):
        dataset_path = 'test_files'
        pascal_reader = PascalDatasetReader()
        self.assertRaises(FoldersNamesError, pascal_reader.get_data, dataset_path)

    def test_test_structure_exist(self):
        pascal_reader = PascalDatasetReader()
        self.assertEqual(pascal_reader._test_structure_exist(self.dataset_name), True)

    def test_xlm_paths_loading(self):
        pascal_reader = PascalDatasetReader()
        pascal_reader._test_structure_exist(self.dataset_name)
        xmls = load_xml_paths(pascal_reader.annotations_folder_path)
        self.assertEqual(len(xmls)>0, True)

    def test_extract_data_from_image_folder(self):
        test_data = {}
        pascal_reader = PascalDatasetReader()
        pascal_reader._test_structure_exist(self.dataset_name)
        test_data = pascal_reader._extract_data_from_image_folder(test_data)
        self.assertEqual(isinstance(test_data['images'], list) , True)
        self.assertEqual(len(test_data['images']) > 0, True)

    def initcietor_for_xml_tests(self):
        test_data = {}
        pascal_reader = PascalDatasetReader()
        pascal_reader._test_structure_exist(self.dataset_name)
        xmls = load_xml_paths(pascal_reader.annotations_folder_path)
        read_xml = pascal_reader._read_xml(xmls[0])
        return read_xml

    def test_read_xml_img_name(self):
        read_xml = self.initcietor_for_xml_tests()
        valid_images_extencion = (".jpg", ".png", ".jpeg")
        self.assertEqual(read_xml[0]['img_name'].endswith(valid_images_extencion), True)

    def test_read_xml_img_path(self):
        read_xml = self.initcietor_for_xml_tests()
        self.assertEqual(os.path.exists(read_xml[0]['img_path']), True)

    def test_read_xml_size_with(self):
        read_xml = self.initcietor_for_xml_tests()
        self.assertEqual(int(read_xml[0]['width'])>0, True)

    def test_read_xml_size_with(self):
        read_xml = self.initcietor_for_xml_tests()
        self.assertEqual(int(read_xml[0]['height'])>0, True)

    def test_read_xml_size_with(self):
        read_xml = self.initcietor_for_xml_tests()
        self.assertEqual(int(read_xml[0]['depth'])>0, True)

    def test_read_xml_bbox_labels(self):
        read_xml = self.initcietor_for_xml_tests()
        self.assertEqual(len(read_xml[0]['labels'])>0, True)

    def test_read_xml_bbox(self):
        read_xml = self.initcietor_for_xml_tests()
        self.assertEqual(len(read_xml[0]['boxes'])>0, True)
    
    def test_read_xml_bbox_and_labels_same_count(self):
        read_xml = self.initcietor_for_xml_tests()
        self.assertEqual(len(read_xml[0]['labels']) == len(read_xml[0]['boxes']), True)

    def test_if_output_data_have_images(self):
        pascal_reader = PascalDatasetReader()
        data_in_output_format = pascal_reader.get_data(self.dataset_name)
        self.assertEqual(data_in_output_format['images'], True)

    def test_if_output_data_have_objects(self):
        pascal_reader = PascalDatasetReader()
        data_in_output_format = pascal_reader.get_data(self.dataset_name)
        self.assertEqual(len(data_in_output_format['objects'])>0, True)

    def test_if_output_data_have_images(self):
        pascal_reader = PascalDatasetReader()
        data_in_output_format = pascal_reader.get_data(self.dataset_name)
        self.assertEqual(len(data_in_output_format['dataset_classes'])>0, True)

    def tearDown(self):
        remove_folder(self.dataset_name)


class CocoDatasetMakerTests(unittest.TestCase):
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
        folder_txts = load_text_paths(self.annotations_path)
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