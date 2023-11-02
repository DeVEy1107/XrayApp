import cv2
import numpy as np
import torchvision.transforms as transforms

import torch

from utils.transforms import get_affine_transform
from utils.inference import get_final_preds


def get_img_center_and_scale(img):
    width, height = img.shape[1], img.shape[0]
    c = np.array([width / 2., height / 2.], dtype=np.float32)
    s = np.array([width / 200., height / 200.], dtype=np.float32)

    return c, s 

def get_model_input_256x256_from_origin(cfg, img, ref_coord=None):
    c, s = get_img_center_and_scale(img)
    r = 0
    
    if ref_coord is None:
        ref_coord = np.array([0.0, 0.0], dtype=np.float32)
    else:
        ref_coord = ref_coord

    trans = get_affine_transform(c, s, r, cfg.MODEL.IMAGE_SIZE)
    input = cv2.warpAffine(
        img,
        trans,
        (int(cfg.MODEL.IMAGE_SIZE[0]), int(cfg.MODEL.IMAGE_SIZE[1])),
        flags=cv2.INTER_LINEAR
    )

    transform = transforms.Compose([transforms.ToTensor()])
    input = transform(input)
    input = input.unsqueeze(0)

    meta = {
        'center': c,
        'scale': s,
        'ref_coord': ref_coord
    }

    return input, meta

def get_model_input_192x256_from_origin(cfg, img, ref_coord=None):
    offset = 436
    new_width = 1728
    img = img[:, offset:offset+new_width, :]

    c, s = get_img_center_and_scale(img)
    r = 0
    
    if ref_coord is None:
        ref_coord = np.array([offset, 0.0], dtype=np.float32)
    else:
        ref_coord = ref_coord

    trans = get_affine_transform(c, s, r, cfg.MODEL.IMAGE_SIZE)
    input = cv2.warpAffine(
        img,
        trans,
        (int(cfg.MODEL.IMAGE_SIZE[0]), int(cfg.MODEL.IMAGE_SIZE[1])),
        flags=cv2.INTER_LINEAR
    )

    transform = transforms.Compose([transforms.ToTensor()])
    input = transform(input)
    input = input.unsqueeze(0)

    meta = {
        'center': c,
        'scale': s,
        'ref_coord': ref_coord
    }

    return input, meta

def get_model_input(cfg, img, ref_coord=None):

    c, s = get_img_center_and_scale(img)
    r = 0
    
    if ref_coord is None:
        ref_coord = np.array([0.0, 0.0], dtype=np.float32)
    else:
        ref_coord = ref_coord

    trans = get_affine_transform(c, s, r, cfg.MODEL.IMAGE_SIZE)
    input = cv2.warpAffine(
        img,
        trans,
        (int(cfg.MODEL.IMAGE_SIZE[0]), int(cfg.MODEL.IMAGE_SIZE[1])),
        flags=cv2.INTER_LINEAR
    )

    transform = transforms.Compose([transforms.ToTensor()])
    input = transform(input)
    input = input.unsqueeze(0)

    meta = {
        'center': c,
        'scale': s,
        'ref_coord': ref_coord
    }

    return input, meta


def predict(cfg, model, input, meta):
    model.eval()

    with torch.no_grad():

        output = model(input)

        output = output.detach().numpy()

    c = meta['center']
    s = meta['scale']

    pred, _ = get_final_preds(cfg, output, c, s)

    pred = pred.squeeze(0)

    ref_coord = meta['ref_coord']
    pred[:, 0] = pred[:, 0] + ref_coord[0]
    pred[:, 1] = pred[:, 1] + ref_coord[1]

    return pred

def get_sub_imgs(cfg, img, pred):
    # img => (H, W, C), pred => (14, 2)
    pred = pred.tolist()
    
    # input image size ex.256x256 => w_s = 128, h_s = 128
    w_s, h_s = int(cfg.MODEL.IMAGE_SIZE[0] // 2), int(cfg.MODEL.IMAGE_SIZE[1] // 2) 
    
    new_imgs = []
    for p in pred:
        w_c, h_c = int(p[0]), int(p[1])
        new_img = img[h_c-h_s:h_c+h_s, w_c-w_s:w_c+w_s, :]
        new_imgs.append(new_img)

    return new_imgs 
