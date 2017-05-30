""" Library for image processing """
import os
import logging
from PIL import Image
import numpy as np

LOGGER = logging.getLogger('imageutils')

def img_to_array(img, data_format='channels_last', data_type=np.float32):
    """Converts a PIL Image instance to a Numpy array.
    Arguments:
      img: PIL Image instance.
      data_format: Image data format.
    Returns:
      A 3D Numpy array.
    Raises:
      ValueError: if invalid `img` or `data_format` is passed.
    """
    if data_format not in {'channels_first', 'channels_last'}:
        LOGGER.WARNING('Unknown/missing data format in img_to_array function: ' + data_format)
        return None
        #raise ValueError('Unknown data_format: ', data_format)
    # Numpy array x has format (height, width, channel)
    # or (channel, height, width)
    # but original PIL image has format (width, height, channel)
    # 'channels_first' by default for tensorflow image format
    img_data = np.asarray(img, dtype=data_type)
    if len(img_data.shape) == 3:
        if data_format == 'channels_first':
            img_data = img_data.transpose(2, 0, 1)
    elif len(img_data.shape) == 2:
        if data_format == 'channels_first':
            img_data = img_data.reshape((1, img_data.shape[0], img_data.shape[1]))
        else:
            img_data = img_data.reshape((img_data.shape[0], img_data.shape[1], 1))
    else:
        LOGGER.WARNING('Unsupported image shape in img_to_array function: ' + str(img_data.shape))
        return None
        #raise ValueError('Unsupported image shape: ', img_data.shape)
    return img_data


def resize_img(img, target_size):
    """Return resized PIL image"""
    if target_size is None \
       or not isinstance(target_size, (list, tuple, np.ndarray)) \
       or len(target_size) != 2:
        LOGGER.WARNING('Unexpected size dimension for resize_img function: ' + str(target_size))
        return None
    hw_tuple = (target_size[1], target_size[0])
    if img.size != hw_tuple:
        img = img.resize(hw_tuple, Image.ANTIALIAS)
    return img


def crop_img(img, target_crop):
    """Returns cropped PIL image"""
    if target_crop is None \
       or not isinstance(target_crop, (list, tuple, np.ndarray)) \
       or len(target_crop) != 4:
        LOGGER.WARNING('Unexpected crop dimension for crop_img function: ' + str(target_crop))
        return None
    img = img.crop(target_crop)
    return img


def load_img(path, target_size=None):
    """Loads an image into PIL format.
    # Arguments
        path: Path to image file
        grayscale: Boolean, whether to load the image as grayscale.
        target_size: Either `None` (default to original size)
            or tuple of ints `(img_height, img_width)`.
    # Returns
        A PIL Image instance.
    # Raises
        ImportError: if PIL is not available.
    """
    if Image is None:
        LOGGER.WARNING('Could not import PIL.Image. The use of `load_img` requires PIL.')
        return None
        #raise ImportError('Could not import PIL.Image. '
        #                  'The use of `load_img` requires PIL.')
    if not os.path.exists(path):
        LOGGER.WARNING('Directory not found ing load_img function: ' + path)
        return None
        #raise ValueError('Directory not found: ', path)
    img = Image.open(path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    if target_size:
        img = resize_img(img, target_size=target_size)
    return img


def save_img(img, output_path, quality=95):
    """Saves PIL image with a provided filename"""
    if not output_path or not os.path.exists(os.path.dirname(output_path)):
        LOGGER.WARNING('Directory not found in save_img function: ' + output_path)
        #raise ValueError('Directory not found: ', os.path.dirname(output_path))
    else:
        img.save(output_path, 'jpeg', quality=quality)
