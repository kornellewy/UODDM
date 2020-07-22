import os 
import unittest

from pascal_dataset_interface import PascalDatasetReader, PascalFoldersNamesError
from pascal_dataset_maker import PascalDatasetWriter
from labelbox_interface import LabelBoxInterface
from utils import load_images, remove_folder, load_xml_paths


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
        self.assertRaises(PascalFoldersNamesError, pascal_reader.get_data, dataset_path)

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

if __name__ == '__main__':
    unittest.main()