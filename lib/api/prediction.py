from copy import deepcopy

import cv2
import numpy as np

from config import cfg, update_config

from model.get_model import get_TranPoseH, get_PoseHRNet
from utils.preprocess import *

type_names = [
    "Sella", "Nasion", "Orbitale", "A", "B", "Pogonion", "Menton",
    "Gonion", "Basion", "Porion", "UIA", "UIE", "LIE", "LIA"       
]

model_files = {
    "Sella": r"models\HRNet\HRNet_w32_256x256_Sella\model_best.pth",
    "Nasion": r'models\HRNet\HRNet_w32_256x256_Nasion\model_best.pth',
    "Orbitale": r"models\HRNet\HRNet_w32_256x256_Orbitale\model_best.pth",
    "A": None,
    "B": None,
    "Pogonion": None,
    "Menton": r"models\HRNet\HRNet_w32_256x256_Menton\model_best.pth",
    "Gonion": None,
    "Basion": None,
    "Porion": None,
    "UIA": None,
    "UIE": r"models\HRNet\HRNet_w32_256x256_UIE\model_best.pth",
    "LIE": r"models\HRNet\HRNet_w32_256x256_LIE\model_best.pth",
    "LIA": None
}

preprocess_model_file = r"models\Transpose\TPH_w32_256x256\model_best.pth"

preprocess_model = None

loaded_models = []

def get_predictions(filepaths):
    trans_yaml_path = r"yamlfiles\TPH_w32_192x256.yaml"
    hrnet_yaml_path = r"yamlfiles\HRNet_w32_256x256_Full.yaml"

    trans_cfg = deepcopy(cfg)
    hrnet_cfg = deepcopy(cfg)

    update_config(trans_cfg, trans_yaml_path)
    update_config(hrnet_cfg, hrnet_yaml_path)

    global preprocess_model
    if preprocess_model is None:
        preprocess_model = get_TranPoseH(trans_cfg, pretrained=True, model_file=preprocess_model_file)

    global loaded_models
    if not loaded_models:
        for name in type_names:
            model_file = model_files[name]
            model = get_PoseHRNet(hrnet_cfg, pretrained=True, model_file=model_file)
            loaded_models.append(model)
    
    preds = []
    for filepath in filepaths:
        img = cv2.imread(filepath, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION)

        input, meta = get_model_input_256x256_from_origin(trans_cfg, img)

        preprocess_pred = predict(trans_cfg, preprocess_model, input, meta)

        sub_imgs = get_sub_imgs(hrnet_cfg, img, preprocess_pred)
        ref_coords = np.zeros(preprocess_pred.shape)
        ref_coords[:, 0] = preprocess_pred[:, 0] - (cfg.MODEL.IMAGE_SIZE[0] // 2)  
        ref_coords[:, 1] = preprocess_pred[:, 1] - (cfg.MODEL.IMAGE_SIZE[1] // 2)

        pred = np.zeros((14, 2), dtype=np.float32)
        for i, model in enumerate(loaded_models):
            if model is not None:
                input, meta = get_model_input(hrnet_cfg, sub_imgs[i], ref_coords[i])
                pred[i, :] = predict(cfg, model, input, meta)
            else:
                pred[i, :] = preprocess_pred[i, :]

        preds.append(pred)
    
    preds = np.array(preds)

    return preds


