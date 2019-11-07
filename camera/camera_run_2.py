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
    current_time = Column(DateTime, nullable=False, default=datetime.now())
    image_name = Column(String(100))

    def __repr__(self):
        return "< id='%s', cam_name='%s', track_num='%s', feature='%s', bb_coord='%s')>" % (self.id, self.track_num, self.cam_name, self.feature,self.bb_coord)

Base.metadata.create_all(engine)
########################


class ipcamCapture:
    def __init__(self, video_path):
        self.Frame = []
        self.status = False
        self.isstop = False
        self.capture = cv2.VideoCapture(video_path)

    def start(self):
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
        self.isstop = True
        print('ipcam stopped!')

    def getframe(self):
        return self.Frame

    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()        
        self.capture.release()

## Load Video ["S1-B4b-L_5","S21-B4-L-13","S21-B4-L-15","S21-B4-R-10"]
class Camera_Process(object):
    def __init__(self, cam_list=["S1-B4b-L-B","S21-B4-T","S1-B3b-L-TL","S2-B4b-L-B"], rtsp=True, reid_model='ResNet50', reid_weight='ResNet50_Market.pth', reid_device='cpu'):
        self.isstop = False
        reader = csv.reader(open('camera/camera.csv', 'r'))
        self.camera = {}
        for row in reader:
            k, v = row
            self.camera[k] = v

        for cam_name in cam_list:
            image_path = os.path.join('static',cam_name)
            if not os.path.exists(image_path):
                os.makedirs(image_path)
    
        vdo = cv2.VideoCapture()
        vdo.set(cv2.CAP_PROP_FPS, 10)
        
        if rtsp:
            vdo.open(self.camera[cam_list[0]])
        else:
            vdo.open('./media/videos/'+cam_list[0]+'.mp4')
        self.im_width = int(vdo.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.im_height = int(vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.area = 0, 0, self.im_width, self.im_height
        
        self.cam_list=cam_list
        self.rtsp=rtsp
        
        yolov3_weights_downloader('./yolo3/')
        self.yolo3 = YOLO3('yolo3/yolo_v3.cfg','yolo3/yolov3.weights','yolo3/coco.names', yolo_device=reid_device, is_xywh=True)
        
        self.extractor = Extractor(reid_model,reid_weight,reid_device=reid_device)
        
    def start(self):
        print('started!')
        self.isstop = False
        threading.Thread(target=self.camera_run, daemon=True, args=()).start()

    def stop(self):
        self.isstop = True
        print('ipcam stopped!')
    
    def camera_run(self):
        
        ########################
        
        if self.rtsp:
            ipcam_1 = ipcamCapture(self.camera[self.cam_list[0]])
            ipcam_1.start()
            time.sleep(1)
            
            ipcam_2 = ipcamCapture(self.camera[self.cam_list[1]])
            ipcam_2.start()
            time.sleep(1)
            
            ipcam_3 = ipcamCapture(self.camera[self.cam_list[2]])
            ipcam_3.start()
            time.sleep(1)
            
            ipcam_4 = ipcamCapture(self.camera[self.cam_list[3]])
            ipcam_4.start()
            time.sleep(1)
        else:
            ipcam_1 = ipcamCapture('./media/videos/'+self.cam_list[0]+'.mp4')
            ipcam_1.start()
            time.sleep(1)
            
            ipcam_2 = ipcamCapture('./media/videos/'+self.cam_list[1]+'.mp4')
            ipcam_2.start()
            time.sleep(1)
            
            ipcam_3 = ipcamCapture('./media/videos/'+self.cam_list[2]+'.mp4')
            ipcam_3.start()
            time.sleep(1)
            
            ipcam_4 = ipcamCapture('./media/videos/'+self.cam_list[3]+'.mp4')
            ipcam_4.start()
            time.sleep(1)

        xmin, ymin, xmax, ymax = self.area

        while not self.isstop:
            frame_1 = ipcam_1.getframe()
            frame_2 = ipcam_2.getframe()
            frame_3 = ipcam_3.getframe()
            frame_4 = ipcam_4.getframe()
            
            for cam_i in range(4):
                if cam_i == 0:
                    frame = frame_1          
                elif cam_i == 1:
                    frame = frame_2
                elif cam_i == 2:
                    frame = frame_3
                else:
                    frame = frame_4
                if frame is not None:
                    im = frame[ymin:ymax, xmin:xmax, (2,1,0)]
                    bbox_xywh, cls_conf, cls_ids = self.yolo3(im)
                    current_time = datetime.now()
                    if bbox_xywh is not None:
                        for i,box in enumerate(bbox_xywh):
                            x,y,w,h = box
                            if h/w > 2 and w > 30:
                                x1 = max(int(x-w/2),0)
                                x2 = min(int(x+w/2),self.im_width-1)
                                y1 = max(int(y-h/2),0)
                                y2 = min(int(y+h/2),self.im_height-1)
                                cropped = frame[y1:y2,x1:x2]
                                print(x1,y1,x2,y2)
                                cam_name = self.cam_list[cam_i]
                                image_path = os.path.join('static',cam_name)
                                image_name = str(time.strftime("%Y-%m-%d-%H-%M-%S-%f"))+'_'+str(i)+'.jpg'
                                cv2.imwrite(os.path.join(image_path,image_name),cropped)
                                pil_image=cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
                                feature = self.extractor(pil_image)[0]
                                embed = str(feature.tostring())
                                record = Feature(cam_name=cam_name, track_num=i, feature=embed,bb_coord=str(box),current_time=current_time,image_name=image_name)
                                session.add(record)
                        session.commit()
        
if __name__=="__main__":
    fire.Fire(camera_run)
