import os

import torch

from model.transpose_h import TransPoseH
from model.pose_hrnet import PoseHighResolutionNet


def get_TranPoseH(cfg, pretrained=False, model_file=None, device='cpu', **kwargs):
    model = TransPoseH(cfg, **kwargs)

    if pretrained:
        if model_file is not None and os.path.isfile(model_file):
            pretrained_state_dict = torch.load(model_file, map_location=torch.device(device))
            model.load_state_dict(pretrained_state_dict, strict=True)
        else:
            return None
        
    return model

def get_PoseHRNet(cfg, pretrained=False, model_file=None, device='cpu', **kwargs):
    model = PoseHighResolutionNet(cfg, **kwargs)

    if pretrained:
        if model_file is not None and os.path.isfile(model_file):
            pretrained_state_dict = torch.load(model_file, map_location=torch.device(device))
            model.load_state_dict(pretrained_state_dict, strict=True)
        else:
            return None

    return model 