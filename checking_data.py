""" Modul check if datata read by interface have good format,
check if images was download, and images have good count number.
"""
import os

# https://www.programiz.com/python-programming/user-defined-exception
class DataChecker(object):
    def __init__(self):
        super().__init__()

    def check_images_exist(self, data):
        try:
            images = data['images']
        except KeyError:
            raise KeyError('no images key in input data dict')
        return None

    def check_objects_exist(self, data):
        try:
            objects = data['objects']
        except KeyError:
            raise KeyError('no objects key in input data dict')
        return None

    def check(self, data):
        """ Method check if data have good format
        """
        self.check_images_exist(data)
        self.check_objects_exist(data)

        return True


        
