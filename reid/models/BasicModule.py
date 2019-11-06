import os
import torch as t

class BasicModule(t.nn.Module):
    '''
    封装了nn.Module,主要是提供了save和load两个方法
    '''

    def __init__(self):
        super(BasicModule,self).__init__()
        self.model_name=str(type(self))# default name

    def load(self, load_path):
        self.load_state_dict(t.load(load_path,map_location=t.device('cpu')))

    def net_load(self, load_path):
        self.load_state_dict(t.load(load_path,map_location=t.device('cpu'))['net_dict'])
        

        