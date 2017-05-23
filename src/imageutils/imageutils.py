""" Library for image processing """
from PIL import Image
import os


def resize_img(img, target_size=None):
    """Return resized PIL image"""
    hw_tuple = (target_size[1], target_size[0])
    if img.size != hw_tuple:
        img = img.resize(hw_tuple, Image.ANTIALIAS)
    return img


def crop_img(img, target_crop=None):
    """Returns cropped PIL image"""
    assert len(target_crop) == 4
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
        raise ImportError('Could not import PIL.Image. '
                          'The use of `array_to_img` requires PIL.')
    img = Image.open(path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    if target_size:
        img = resize_img(img)
    return img


def save_img(img, output_path=None):
    """Saves PIL image with a provided filename"""
    if not output_path or not os.path.exists(os.path.dirname(output_path)):
        raise ValueError('Directory not found: ', output_path)
    else:
        img.save(output_path)
