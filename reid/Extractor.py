import os
import cv2
import torch
import torchvision.transforms as transforms
import numpy as np
import reid.models
from .reid_weights_downloader import reid_weights_downloader

class Extractor(object):
    def __init__(self, model_name, model_weight,reid_device):
        # if model_name == 'MGN':
        #     pooling = 'MAX'
        #     last_stride = 2
        # else:
        #     pooling = 'AVG'
        #     last_stride = 1
        self.model = getattr(reid.models, model_name)(751)
        print("Network "+model_name+" loaded!")
        self.model_path = os.path.join('.','reid','weights',model_weight)
        reid_weights_downloader(model_weight)
        self.device = reid_device
        # or model_name == 'Paper_MGN'
        # if model_name == 'Net' :
        if model_name == "Net":
            self.model.net_load(self.model_path)
        # else:
        # self.model.load(self.model_path) 
        print("Loading weights from {}... Done!".format(self.model_path))
        self.model.to(self.device)
        self.norm = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        self.resize = transforms.Resize([384, 128])
        self.totensor = transforms.ToTensor()

    def __call__(self, img_list):
        for count, img in enumerate(img_list):
            assert isinstance(img, np.ndarray), "type error"
            img = img.astype(np.float)#/255.
            img = cv2.resize(img, (128,384))
            img = torch.from_numpy(img).float().permute(2,0,1).unsqueeze(0)
            if count == 0:
                final_img = img
            else:
                final_img = torch.cat((final_img, img), 0)

        self.model.eval()
        with torch.no_grad():
            img = final_img.to(self.device)
            feature_list = self.model(img)
            feature_list = feature_list.cpu().numpy()
        
        return feature_list

if __name__ == '__main__': 
    pass   
    # img = cv2.imread("../media/images/jiashu.jpg")[:,:,(2,1,0)]
    # model_name = 'ResNet50'
    # model_weight = 'ResNet50_Market'
    # reid_device = 'cpu'
    # extr = Extractor(model_name,model_weight,reid_device)
    # feature = extr(img)
    # print(feature.shape)
