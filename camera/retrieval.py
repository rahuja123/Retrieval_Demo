import os
import cv2
import sys
import csv
import fire
import torch
import numpy as np
from PIL import Image
from datetime import datetime
from ast import literal_eval
from reid import Extractor
from reid import reid_weights_downloader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

import warnings
warnings.filterwarnings("ignore")

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, Sequence('id'), primary_key=True)
    cam_name = Column(String(50))
    track_num = Column(Integer)
    feature = Column(String(3000000))
    bb_coord = Column(String(50))
    time = Column(DateTime, nullable=False, default=datetime.now())
    image_name = Column(String(100))

    def __repr__(self):
        return "< id='%s', cam_name='%s', track_num='%s', feature='%s', bb_coord='%s')>" % (self.id, self.track_num, self.cam_name, self.feature,self.bb_coord)

Base.metadata.create_all(engine)

cam_name = ['S21-B4-L-13']

def retrieval(query="media/images/yihang.jpg",cam_name_list=['S21-B4-R-10'],rank=10, reid_model='Net', reid_weight='Net_Market.t7', reid_device='cpu'):

    if query:
        print("true query")
    print(cam_name_list)
    print(rank)
    print(reid_model)
    print(reid_weight)
    print(reid_device)
    embed_npdtype = np.float32
    extractor = Extractor(reid_model,reid_weight,reid_device=reid_device)
    target_img = cv2.imread(query)[:,:,(2,1,0)]
    # print(target_img)
    pil_image=cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)
    qf = torch.from_numpy(extractor(pil_image)).float().to(reid_device)

    gf = []
    gf_image = []
    for cam_name in cam_name_list:
        query_result = session.query(Feature).filter(Feature.cam_name == cam_name).all()
        for result in query_result:
            feat = result.feature
            image = result.image_name
            bytearr = literal_eval(feat)
            result = np.fromstring(bytearr, dtype=embed_npdtype)
            gf.append(result)
            gf_image.append(os.path.join(cam_name,image))
    gf = torch.from_numpy(np.asarray(gf)).float().to(reid_device)

    m, n = qf.shape[0], gf.shape[0]
    distmat = torch.pow(qf, 2).sum(dim=1, keepdim=True).expand(m, n) + torch.pow(gf, 2).sum(dim=1, keepdim=True).expand(n,m).t()
    distmat.addmm_(1, -2, qf, gf.t())
    distmat = distmat.cpu().numpy()
    indices = np.argsort(distmat, axis=1)[0]

    image_list=[]
    number = 10
    for i in range(number):
        index = int(indices[i])
        image_path = os.path.join('static',gf_image[index])
        image_list.append(image_path)

    return image_list

if __name__=="__main__":
    fire.Fire(retrieval)