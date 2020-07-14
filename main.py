from labelbox_interface import LabelBoxInterface
from pascal_dataset_maker import PascalDatasetWriter
from data_augmentation import PascalDataArgumenter
from utils import clean_tmp

if __name__ == "__main__":
    # # Test creating pascal dataset from label box
    # TEST_FILE = 'test_files/test_dataset.json'
    # TMP_FOLDER = 'tmp'
    # kjn = LabelBoxInterface()
    # test_data = kjn.get_data(TEST_FILE)
    # kjn1 = PascalDatasetWriter()
    # kjn1.abstract_make_dataset(data=test_data, base_path='', dataset_name='test')
    # clean_tmp(TMP_FOLDER)

    # Test argument pascal dataset from label box
    TEST_FILE = 'test_files/test_dataset2.json'
    TMP_FOLDER = 'tmp'
    BACKGROUND_IMAGES = 'test_files/random_background_images'
    clean_tmp(TMP_FOLDER)
    kjn = LabelBoxInterface()
    test_data = kjn.get_data(TEST_FILE)
    kjn1 = PascalDataArgumenter()
    kjn1.abstract_argument_data(data=test_data, base_path='', dataset_name='test', image_limit_count=100, background_images_folder=BACKGROUND_IMAGES)
    clean_tmp(TMP_FOLDER)