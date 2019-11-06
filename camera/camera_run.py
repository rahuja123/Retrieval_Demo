import os
import cv2
import sys
import csv
import json
import fire
import time
import threading
import numpy as np
from PIL import Image
from datetime import datetime
from yolo3 import YOLO3
from yolo3 import yolov3_weights_downloader
from reid import Extractor
from reid import reid_weights_downloader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

import warnings
warnings.filterwarnings("ignore")

### Create Dataset ##
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
########################
reader = csv.reader(open('camera/camera.csv', 'r'))
camera = {}
for row in reader:
    k, v = row
    camera[k] = v

## Load Yolo
yolov3_weights_downloader('./yolo3/')
yolo_network = 'yolo3/yolo_v3.cfg'
yolo_classes = 'yolo3/coco.names'
yolo_weight = 'yolo3/yolov3.weights'
yolo_device = 'cpu'

## Load ReID
reid_model='Net'
reid_weight = 'Net_Market.t7'
reid_device = yolo_device


## Load Video
def camera_run(cam_name="S1-B3b-R-BR", rtsp=True, skip_frame=10, reid_model='ResNet50', reid_weight='ResNet50_Market.pth', reid_device='cpu'):
    yolo3 = YOLO3(yolo_network,yolo_weight,yolo_classes, yolo_device=yolo_device, is_xywh=True)
    extractor = Extractor(reid_model,reid_weight,reid_device=reid_device)
    image_path = os.path.join('static',cam_name)
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    vdo = cv2.VideoCapture()
    if rtsp:
        source_path = camera[cam_name]
        vdo.open(source_path)
    else:
        vdo.open('./media/videos/'+cam_name+'.mp4')
    im_width = int(vdo.get(cv2.CAP_PROP_FRAME_WIDTH))
    im_height = int(vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    area = 0, 0, im_width, im_height
    xmin, ymin, xmax, ymax = area

    frame_count = 0
    while vdo.grab():
        frame_count += 1
        if (frame_count % skip_frame) == 0:
            ret, frame = vdo.retrieve()
            if not ret: break
            im = frame[ymin:ymax, xmin:xmax, (2,1,0)]
            bbox_xywh, cls_conf, cls_ids = yolo3(im)
            time = datetime.now()
            if bbox_xywh is not None:
                for i,box in enumerate(bbox_xywh):
                    x,y,w,h = box
                    x1 = max(int(x-w/2),0)
                    x2 = min(int(x+w/2),im_width-1)
                    y1 = max(int(y-h/2),0)
                    y2 = min(int(y+h/2),im_height-1)
                    cropped = frame[y1:y2,x1:x2]
                    print(x1,y1,x2,y2)
                    image_name = str(time.strftime("%Y-%m-%d-%H-%M-%S-%f"))+'_'+str(i)+'.jpg'
                    cv2.imwrite(os.path.join(image_path,image_name),cropped)
                    pil_image=cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
                    feature = extractor(pil_image)[0]
                    embed = str(feature.tostring())
                    record = Feature(cam_name=cam_name, track_num=i, feature=embed,bb_coord=str(box),time=time,image_name=image_name)
                    session.add(record)
            session.commit()
if __name__=="__main__":
    fire.Fire(camera_run)
