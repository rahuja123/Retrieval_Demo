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
from yolo3 import YOLO3
from yolo3 import yolov3_weights_downloader
from reid import Extractor
from reid import reid_weights_downloader

import warnings

Base = declarative_base()
engine = create_engine('sqlite:///offline_database.db')
class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, Sequence('id'), primary_key=True)
    cam_name = Column(String(50))
    feature = Column(String(3000000))
    bb_coord = Column(String(50))
    frame_num = Column(Integer)
    star_time = Column(DateTime, nullable=False, default=datetime.now())
    end_time = Column(DateTime, nullable=False, default=datetime.now())
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
    starttime= datetime(int(year),int(month),int(day),int(s_hour),int(s_mintue),0)
    endtime= datetime(int(year),int(month),int(day),int(e_hour),int(e_mintue),0)
    
    video_list = []
    for cam in cam_name_list:
        save_dir = os.path.join('.','static','RawVideos',cam)
        os.makedirs(save_dir, exist_ok=True)
        rtsp = camera[cam]
        channel = int(rtsp.split('/')[-1][:2])
        ip = rtsp.split('/')[-4].split('@')[1].split(':')[0]
        file_name = "{}_{}_{}-{}_{}-{}.mp4".format(cam,date,s_hour,s_mintue,e_hour,e_mintue)
        video_list.append(os.path.join(save_dir,file_name))
        print("Downloading "+file_name)
        proc = subprocess.Popen(["./Hikvision_Video_Downloader", ip, 'admin', 'admin12345', 
                                str(channel), str(year), str(month), str(day), 
                                str(s_hour), str(s_mintue), str(0), 
                                str(e_hour), str(e_mintue), str(0),
                                os.path.join(save_dir,file_name)])
        
        proc.wait()
        # print("./camera/Hikvision_Video_Downloader", ip, 'admin', 'admin12345', 
        #                         str(channel), str(year), str(month), str(day), 
        #                         str(s_hour), str(s_mintue), str(0), 
        #                         str(e_hour), str(e_mintue), str(0),
        #                         os.path.join(save_dir,file_name))
    print('Download Completed')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yolov3_weights_downloader('./yolo3/')
    yolo3 = YOLO3('yolo3/yolo_v3.cfg','yolo3/yolov3.weights','yolo3/coco.names', yolo_device=reid_device, is_xywh=True)

    extractor = Extractor(reid_model,reid_weight,reid_device=reid_device)
    
    vdo = cv2.VideoCapture()
    # vdo.set(cv2.CAP_PROP_FPS, 10)
    
    for video in video_list:
        cam = video.split('/')[-1].split("_")[0]
        vdo.open(video)
        im_width = int(vdo.get(cv2.CAP_PROP_FRAME_WIDTH))
        im_height = int(vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        area = 0, 0, im_width, im_height
        xmin, ymin, xmax, ymax = area
        
        ct = 0
        skip_frame = 30
        while vdo.grab(): 
            if ct % skip_frame == 0: # skip some frames
                ret, frame = vdo.retrieve()
                if not ret: break 
                im = frame[ymin:ymax, xmin:xmax]
                im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_dict = {}
                frame_dict[cam]=im
                result_dict = yolo3(frame_dict)
                bbox_xywh, cls_conf, cls_ids = result_dict[cam]
                if bbox_xywh is not None:
                    for i,box in enumerate(bbox_xywh):
                        x,y,w,h = box
                        if h/w > 2 and w > 60:
                            x1 = max(int(x-w/2),0)
                            x2 = min(int(x+w/2),im_width-1)
                            y1 = max(int(y-h/2),0)
                            y2 = min(int(y+h/2),im_height-1)
                            frame = im
                            cropped = frame[y1:y2,x1:x2]
                            # print("Detection {}, {}, {}, {}".format(x1,y1,x2,y2))
                            logger.info("{} : {}, {}, {}, {}".format(cam,x1,y1,x2,y2))

                            image_path = os.path.join('static','ExtractedImages',cam)
                            os.makedirs(image_path, exist_ok=True)
                            image_name = '{}_{}_{}-{}_{}.jpg'.formate(cam,date,s_hour,s_mintue,i)
                            cv2.imwrite(os.path.join(image_path,image_name),cropped)
                            pil_image=cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
                            feature = extractor([pil_image])
                            embed = str(feature[0].tostring())
                            record = Feature(cam_name=cam, track_num=ct, feature=embed,bb_coord=str(box),star_time=starttime,end_time=endtime,image_name=image_name)
                            session.add(record)
                            session.commit()
            ct += 1



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
