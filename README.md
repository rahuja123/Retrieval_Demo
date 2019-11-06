# NTUReID Indoor Demo GUI

> We don't support backend functionality right now. Only the frontend GUI can be run. The backend integration will be done soon. 

## Requirements
- [dash by plotly](https://dash.plot.ly/)
- [flask](https://palletsprojects.com/p/flask/)
- [python 3](https://www.python.org/downloads/)
- [pytorch 0.4+ ](https://pytorch.org/)
- [fire](https://github.com/google/python-fire)
- [opencv-python](https://pypi.org/project/opencv-python/)

Install all dependences libraries
``` bash
pip3 install -r requirements.txt
```

## To-DO
- need to specify the size of image upload.
- Add the background functionality. 


## Support Model And Weight:
| __Model__ | __Weight (Train on Market)__ |
|-----------|------------|
| ResNet50 | ResNet50_Market |
| ResNet101 | ResNet101_Market |
| SE_ResNet50 | SE_ResNet50_Market |
| SE_ResNet101 | SE_ResNet101_Market |

default network ResNet50
default weight ResNet50_Market

## Running:

``` bash

### Follow the code below for GUI. 
python app_exp.py

-- TO-DO (Will be added soon)

### python run.py [target_image] [video_source]
python run.py  ./media/images/jiashu.jpg ./media/videos/S21-B4-L-13.mp4

### python run.py [target_image] [video_source] [model] [weight]
python run.py  ./media/images/jiashu.jpg ./media/videos/S21-B4-L-13.mp4 ResNet101 ResNet101_Market

### python run.py [target_image] [video_source] [threshold] [skip_frame]
python run.py  ./media/images/jiashu.jpg ./media/videos/S21-B4-L-13.mp4 400 5

### python run.py [target_image] [video_source] [threshold] [skip_frame] [yolo_device] [reid_device]
python run.py  ./media/images/jiashu.jpg ./media/videos/S21-B4-L-13.mp4 --yolo_device='cuda:0' --reid_device='cuda:1'
```
