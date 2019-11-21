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
import subprocess

import warnings

Base = declarative_base()
engine = create_engine('sqlite:///database.db')
class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, Sequence('id'), primary_key=True)
    cam_name = Column(String(50))
    track_num = Column(Integer)
    feature = Column(String(3000000))
    bb_coord = Column(String(50))
    current_time = Column(DateTime, nullable=False, default=datetime.now())
    image_name = Column(String(100))

    def __repr__(self):
        return "< id='%s', cam_name='%s', track_num='%s', feature='%s', bb_coord='%s')>" % (self.id, self.track_num, self.cam_name, self.feature,self.bb_coord)

Base.metadata.create_all(engine)

if not os.path.exists(os.path.join('static','query')):
    os.makedirs(os.path.join('static','query'))

def offline_retrieval(query="static/query/query.png",cam_name_list=['S1-B4b-L-B'],rank=10, reid_model='ResNet50', reid_weight='ResNet50_Market.pth', reid_device='cpu', date="2019-11-22", start="12:13:14", end="12:15:16"):
    camera = {}
    reader = csv.reader(open('camera/camera.csv', 'r'))
    for row in reader:
        k, v = row
        camera[k] = v
    
    print(date)
    date = date.split('T')[0]
    year,month,day = date.split('-')
    s_hour,s_mintue= start.split(":")
    e_hour,e_mintue= end.split(":")
    
    for cam in cam_name_list:
        save_dir = os.path.join('.','static','RawVideos',cam)
        os.makedirs(save_dir, exist_ok=True)
        rtsp = camera[cam]
        channel = int(rtsp.split('/')[-1][:2])
        ip = rtsp.split('/')[-4].split('@')[1].split(':')[0]
        file_name = "{}_{}_{}-{}_{}-{}".format(cam,date,s_hour,s_mintue,e_hour,e_mintue)
        print("Downloading "+file_name)
        proc = subprocess.Popen([".camera/Hikvision_Video_Downloader", ip, 'admin', 'admin12345', 
                                str(channel), str(year), str(month), str(day), 
                                str(s_hour), str(s_mintue), str(0), 
                                str(e_hour), str(e_mintue), str(0),
                                os.path.join(save_dir,file_name)])
        proc.wait()

    # Session = sessionmaker(bind=engine)
    # session = Session()



    # # print(rank)final_
    # embed_npdtype = np.float32
    # extractor = Extractor(reid_model,reid_weight,reid_device=reid_device)
    # target_img = cv2.imread(query)[:,:,(2,1,0)]
    # pil_image=cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)
    # qf = torch.from_numpy(extractor([pil_image])).float().to(reid_device)

    # cam_rank_image = {}
    # for cam_name in cam_name_list:
    #     gf = []
    #     gf_image = []
    #     # print(cam_name)
    #     query_result = session.query(Feature).filter(Feature.cam_name == cam_name).all()
    #     for result in query_result:
    #         feat = result.feature
    #         image = result.image_name
    #         bytearr = literal_eval(feat)
    #         result = np.fromstring(bytearr, dtype=embed_npdtype)
    #         gf.append(result)
    #         gf_image.append(os.path.join(cam_name,image))
    #     gf = torch.from_numpy(np.asarray(gf)).float().to(reid_device)

    #     m, n = qf.shape[0], gf.shape[0]
    #     distmat = torch.pow(qf, 2).sum(dim=1, keepdim=True).expand(m, n) + torch.pow(gf, 2).sum(dim=1, keepdim=True).expand(n,m).t()
    #     distmat.addmm_(1, -2, qf, gf.t())
    #     distmat = distmat.cpu().numpy()
    #     indices = np.argsort(distmat, axis=1)[0]

    #     image_list=[]

    #     if rank < len(indices):
    #         number = int(rank)
    #     else:
    #         number = len(indices)

    #     for i in range(number):
    #         index = int(indices[i])
    #         image_path = os.path.join('static',gf_image[index])
    #         image_list.append(image_path)

    #     cam_rank_image[cam_name]=image_list

    # session.close()
    # return cam_rank_image

if __name__=="__main__":
    fire.Fire(retrieval)
