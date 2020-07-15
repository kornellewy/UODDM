import json
import os
from PIL import Image
import random
import urllib

import torch
from torch.utils.data import Dataset
import torchvision.transforms.functional as FT
import transforms as T

def load_images_without_extention(path):
    images = []
    valid_images = [".jpg", ".png", "jpeg"]
    for f in os.listdir(path):
        file, ext = os.path.splitext(f)
        if ext.lower() not in valid_images:
            continue
        images.append(file)
    return images

def get_transform(train):
    transforms = []
    transforms.append(T.ToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)

def load_class_names(path):
    with open(path) as file:
        class_names = file.readlines()
    class_names = [x.strip() for x in class_names]
    return class_names

class KJNLabelBoxToPascalVOCDataset(Dataset):
    def __init__(self, labelbox_file_path, transforms, output_path):
        self.transforms = transforms
        labelbox_file_path = os.path.abspath(labelbox_file_path)
        train_images = list()
        train_objects = list()
        n_objects = 0
        # make file structure
        self.output_path = output_path
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        annotations_path = os.path.join(output_path, 'Annotations')
        self.annotations_path = annotations_path
        if not os.path.exists(annotations_path):
            os.mkdir(annotations_path)
        jpeg_images_path = os.path.join(output_path, 'JPEGImages')
        self.jpeg_images_path = jpeg_images_path
        if not os.path.exists(jpeg_images_path):
            os.mkdir(jpeg_images_path)
        # open file
        with open(labelbox_file_path) as json_file:
            data = json.load(json_file)
            output = self.download_images_and_labels(data)
        self.images=output['images']
        self.objects=output['objects']

    def __getitem__(self, i):
        # Read image
        image = Image.open(self.images[i], mode='r').convert('RGB')
        # Read objects in this image (bounding boxes, labels, difficulties)
        print(self.objects)
        objects = self.objects[i]
        boxes = torch.FloatTensor(objects['boxes'])  # (n_objects, 4)
        labels = torch.LongTensor(objects['labels'])  # (n_objects)

        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        image_id = torch.tensor([i])
        iscrowd = torch.zeros((len(boxes),), dtype=torch.int64)

        # creat dict
        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            image, target = self.transforms(image, target)

        # return image, boxes, labels, difficulties
        return image, target

    def __len__(self):
        return len(self.images)

    def download_images_and_labels(self, json_data):
        output ={}
        objects =[]
        images = []
        for image_object in json_data:
            if not bool(image_object["Label"]):
                continue
            meta_data = {}
            image_save_path = os.path.join(self.jpeg_images_path, image_object["ID"]+".jpeg")
            urllib.request.urlretrieve(image_object["Labeled Data"], image_save_path)
            img = Image.open(image_save_path)
            w, h = img.size
            if h>w:
                img = img.rotate(270)
                img.save(image_save_path)
            boxes = list()
            labels = list()
            difficulties = list()
            for object_on_img in image_object["Label"]["objects"]:
                xmin = object_on_img['bbox']['left']
                ymin = object_on_img['bbox']['top']
                xmax = xmin + object_on_img['bbox']['width']
                ymax = ymin + object_on_img['bbox']['height']
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(1)
                difficulties.append(1)
            meta_data.update({'boxes':boxes})
            meta_data.update({'labels':labels})
            meta_data.update({'difficulties':difficulties})
            objects.append(meta_data)
            images.append(image_save_path)
        output.update({'images': images})
        output.update({'objects': objects})
        return output
            
if __name__ == "__main__":
    LABELBOX_JSON_FILE = 'biedronka_dataset\export-2020-06-30T07 16 58.311Z.json'
    train_dataset = KJNLabelBoxToPascalVOCDataset(labelbox_file_path=LABELBOX_JSON_FILE, transforms=get_transform(train=True), output_path='biedronka_dataset')
    print(train_dataset[0])