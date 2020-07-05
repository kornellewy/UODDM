import os
import json
import urllib.request
from PIL import Image

class LabelBoxInterface(object):
    def __init__(self):
        super().__init__()
        self.tmp_folder = 'tmp'
        
    def get_data(self, json_path):
        output ={}
        objects = []
        images = []
        with open(json_path) as json_file:
            json_data = json.load(json_file)
        for image_json_object in json_data:
            object_data = {}
            image_save_path = os.path.join(self.tmp_folder, image_json_object["ID"]+".jpg")
            urllib.request.urlretrieve(image_json_object["Labeled Data"], image_save_path)
            boxes = list()
            labels = list()
            difficulties = list()
            for object_on_img in image_json_object["Label"]["objects"]:
                xmin = object_on_img['bbox']['left']
                ymin = object_on_img['bbox']['top']
                xmax = xmin + object_on_img['bbox']['width']
                ymax = ymin + object_on_img['bbox']['height']
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(object_on_img["value"])
                difficulties.append(1)
            img = Image.open(image_save_path)
            width, height = img.size
            object_data.update({'img_path': image_save_path})
            object_data.update({'width': width})
            object_data.update({'height': height})
            object_data.update({'boxes': boxes})
            object_data.update({'labels': labels})
            object_data.update({'difficulties': difficulties})
            objects.append(object_data)
            images.append(image_save_path)
        output.update({'images': images})
        output.update({'objects': objects})
        return output

    def get_image_size(self, img_path):
        img = Image.open(open(img_path, 'rb'))
        width, height = img.size
        return width, height
    

if __name__ == "__main__":
    TEST_FILE = 'test_files/test_dataset.json'
    kjn = LabelBoxInterface()
    print(kjn.get_data(TEST_FILE))

