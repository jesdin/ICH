import pydicom
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import matplotlib.pyplot as plt

HEIGHT = 256
WIDTH = 256
CHANNELS = 3

SHAPE = (HEIGHT, WIDTH, CHANNELS)

def correct_dcm(dcm):
    x = dcm.pixel_array + 1000
    px_mode = 4096
    x[x>=px_mode] = x[x>=px_mode] - px_mode
    dcm.PixelData = x.tobytes()
    dcm.RescaleIntercept = -1000

def window_image(dcm, window_center, window_width):    
    if (dcm.BitsStored == 12) and (dcm.PixelRepresentation == 0) and (int(dcm.RescaleIntercept) > -100):
        correct_dcm(dcm)
    img = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept
    
    # Resize
    img = cv2.resize(img, SHAPE[:2], interpolation = cv2.INTER_LINEAR)
   
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    img = np.clip(img, img_min, img_max)
    return img

def bsb_window(dcm):
    brain_img = window_image(dcm, 40, 80)
    subdural_img = window_image(dcm, 80, 200)
    soft_img = window_image(dcm, 40, 380)
    
    brain_img = (brain_img - 0) / 80
    subdural_img = (subdural_img - (-20)) / 200
    soft_img = (soft_img - (-150)) / 380
    bsb_img = np.array([brain_img, subdural_img, soft_img]).transpose(1,2,0)
    return bsb_img

def _read(path):
    dcm = pydicom.dcmread(path + ".dcm")
    dcm = dcm.pixel_array 
    # cv2.imwrite(path + '.png', dcm)
    plt.imsave(path + '.png', dcm, cmap=plt.cm.bone)
    return dcm

def get_window(path):
    path = path + ".dcm"
    dcm = pydicom.dcmread(path)
    try:
        image = bsb_window(dcm)
    except:
        image = np.zeros(SHAPE)
    image -= image.min((0,1))
    image = (255*image).astype(np.uint8)
    image = cv2.resize(image, (256, 256))
    return image

def _save(path):
    _read(path)
    image = get_window(path)
    plt.imsave(path + '_windowed.png', image)

def get_blob(img):
    img = img.astype(np.uint8)
    img = Image.fromarray(img)
    buffered = BytesIO()
    img.save(buffered, format="png")    
    img = base64.b64encode(buffered.getvalue())
    return img


# import windowing
# img = windowing._read()