from labelbox_interface import LabelBoxInterface
from pascal_dataset_maker import PascalDatasetWriter

if __name__ == "__main__":
    TEST_FILE = 'test_files/test_dataset.json'
    TMP_FOLDER = 'tmp'
    kjn = LabelBoxInterface()
    test_data = kjn.get_data(TEST_FILE)

    kjn1 = PascalDatasetWriter()
    kjn1.make_dataset(data=test_data, base_path='', dataset_name='test')