#TODO: komentarze
"""
Module deals with image agumantion, DataRandomModifier is main class that u can use. 
ImagePerspectiveTransformer is used in DataRandomModifier and im to stupit to explint it but,
it rotate image along axes in sphere.
"""
import cv2
import numpy as np
import os
from scipy.ndimage import interpolation as inter
from scipy import ndimage
import random
import itertools

from utils import get_rad, deg_to_rad

class ImagePerspectiveTransformer(object):
    """ Perspective transformation class for image
        with shape (height, width, #channels). This is borowed code i jast use it.
    """
    def __init__(self, image, shape):
        super().__init__()
        self.image = image
        self.height = shape[0]
        self.width = shape[1]
        self.num_channels = self.image.shape[2]

    def rotate_along_axis(self, theta=0, phi=0, gamma=0, dx=0, dy=0, dz=0):
        """ Wrapper of Rotating a Image """
        # Get radius of rotation along 3 axes
        rtheta, rphi, rgamma = get_rad(theta, phi, gamma)
        # Get ideal focal length on z axis
        # NOTE: Change this section to other axis if needed
        d = np.sqrt(self.image.shape[0] ** 2 + self.image.shape[1] ** 2)
        self.focal = d / (2 * np.sin(rgamma) if np.sin(rgamma) != 0 else 1)
        dz = self.focal
        # Get projection matrix
        mat = self.get_M(rtheta, rphi, rgamma, dx, dy, dz)
        return cv2.warpPerspective(self.image.copy(), mat, (self.width, self.height))

    def get_M(self, theta, phi, gamma, dx, dy, dz):
        """ Get Perspective Projection Matrix """
        w = self.width
        h = self.height
        f = self.focal
        # Projection 2D -> 3D matrix
        A1 = np.array([[1, 0, -w / 2],
                       [0, 1, -h / 2],
                       [0, 0, 1],
                       [0, 0, 1]])
        # Rotation matrices around the X, Y, and Z axis
        RX = np.array([[1, 0, 0, 0],
                       [0, np.cos(theta), -np.sin(theta), 0],
                       [0, np.sin(theta), np.cos(theta), 0],
                       [0, 0, 0, 1]])
        RY = np.array([[np.cos(phi), 0, -np.sin(phi), 0],
                       [0, 1, 0, 0],
                       [np.sin(phi), 0, np.cos(phi), 0],
                       [0, 0, 0, 1]])
        RZ = np.array([[np.cos(gamma), -np.sin(gamma), 0, 0],
                       [np.sin(gamma), np.cos(gamma), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        # Composed rotation matrix with (RX, RY, RZ)
        R = np.dot(np.dot(RX, RY), RZ)
        # Translation matrix
        T = np.array([[1, 0, 0, dx],
                      [0, 1, 0, dy],
                      [0, 0, 1, dz],
                      [0, 0, 0, 1]])
        # Projection 3D -> 2D matrix
        A2 = np.array([[f, 0, w / 2, 0],
                       [0, f, h / 2, 0],
                       [0, 0, 1, 0]])
        # Final transformation matrix
        return np.dot(A2, np.dot(T, np.dot(R, A1)))

class DataRandomModifier:
    def __init__(self):
        super().__init__()

    def decision(self, probability):
        """ 
        Return bool, if random number is lover then probability given,
        fun will return true, otherwise false.
        :param probability: probability of decision, higher and higher probability
        :type probability: float
        :retruns: 
        :rtype: bool
        """
        return random.random() < probability

    def random_vertical_filp(self, img, p = 0.5):
        """ 
        Method vertical flip img with given probability p.
        :param p: probability vertical fliping
        :type p: float
        :param img: img as numpy ndarray
        :type img: numpy ndarray
        :retruns: fliped or not img
        :rtype: numpy ndarray
        """
        if self.decision(p):
            img = cv2.flip(img, 0)
        return img

    def random_horizontal_filp(self, img, p = 0.5):
        """ 
        Method horizontal flip img with given probability p.
        :param p: probability horizontal fliping
        :type p: float
        :param img: img as numpy ndarray
        :type img: numpy ndarray
        :retruns: fliped or not img
        :rtype: numpy ndarray
        """
        if self.decision(p):
            img = cv2.flip(img, 1)
        return img

    def random_crop(self, img, output_img_h = 0.5, output_img_w = 0.5, p = 0.5):
        """ 
        Method random crop input img.
        :param img: img as numpy ndarray
        :type img: numpy ndarray
        :param output_img_h: output img height i from 0 to 1, cut_h=original_img_height * output_img_h
        :type output_img_h: float
        :param output_img_w: output img width i from 0 to 1, cut_w=original_img_width * output_img_w
        :type output_img_w: float
        :param p: probability horizontal fliping
        :type p: float
        :retruns: fliped or not img
        :rtype: numpy ndarray
        """
        if self.decision(p):
            height, width, channels = img.shape
            new_height = random.randint(int(height * output_img_h), height)
            new_width = random.randint(int(width * output_img_w), width)
            y = random.randint(0, height - new_height)
            x = random.randint(0, width - new_width)
            roi = img[y:y + new_height, x:x + new_width]
            # check if cut is ahve to much dark pixels, more then 20 %
            non_zeros = np.count_nonzero(roi)
            non_zeros_procent = non_zeros / roi.size
            if non_zeros_procent < 0.8:
                pass
            else:
                img = roi
        return img

    def random_img_to_gray(self, img, p = 0.5):
        """ 
        Method taht random change rgb img to gray.
        :param p: probability change to gray
        :type p: float
        :param img: img as numpy ndarray
        :type img: numpy ndarray
        :retruns: gray or not img
        :rtype: numpy ndarray
        """
        if self.decision(p):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = np.zeros_like(img)
            img[:, :, 0] = gray
            img[:, :, 1] = gray
            img[:, :, 2] = gray
        return img

    def random_channel_swap(self, img, p = 0.5):
        """ 
        Method taht random change color chanels betwen them self.
        :param p: probability to change chanels.
        :type p: float
        :param img: img as numpy ndarray
        :type img: numpy ndarray
        :retruns: change img
        :rtype: numpy ndarray
        """
        if self.decision(p):
            img[:, :, 0], img[:, :, 1] = img[:, :, 1], img[:, :, 0]
        if self.decision(p):
            img[:, :, 1], img[:, :, 2] = img[:, :, 2], img[:, :, 1]
        if self.decision(p):
            img[:, :, 2], img[:, :, 0] = img[:, :, 0], img[:, :, 2]
        return img

    def random_blur(self, img, p = 0.5):
        """ 
        Method taht random blured image.
        :param p: probability to blure chanels.
        :type p: float
        :param img: img as numpy ndarray
        :type img: numpy ndarray
        :retruns: blured img
        :rtype: numpy ndarray
        """
        if self.decision(p):
            img = ndimage.gaussian_filter(img, sigma=1)
        return img

    def random_gaussian_noise(self, img, p = 0.5):
        """ 
        Method taht random and gauisan noice to img.
        :param p: probability to blure chanels.
        :type p: float
        :param img: img as numpy ndarray
        :type img: numpy ndarray
        :retruns:  img
        :rtype: numpy ndarray
        """
        if self.decision(p):
            mean = 30.0
            std = 80.0
            img = img + np.random.normal(mean, std, img.shape)

            img = np.clip(img, 0, 255).astype('uint8')
        return img

    
    def random_rotation(self, img, p = 0.5):
        """ 
        Method that random rotate in 3 axes
        :param p: probability to blure chanels.
        :type p: float
        :param img: img as numpy ndarray
        :type img: numpy ndarray
        :retruns:  img
        :rtype: numpy ndarray
        """
        if self.decision(p):
            theta = random.randrange(-15, 15)
            phi = random.randrange(-15, 15)
            gamma = random.randrange(-15, 15)
            it = ImagePerspectiveTransformer(img, shape=(img.shape[0] + abs(gamma), img.shape[1]))
            roi = it.rotate_along_axis(theta=theta, phi=phi, gamma=gamma)
            # check if cut is ahve to much dark pixels, more then 20 %
            non_zeros = np.count_nonzero(roi)
            non_zeros_procent = non_zeros / roi.size
            if non_zeros_procent < 0.8:
                pass
            else:
                img = roi
        return img
