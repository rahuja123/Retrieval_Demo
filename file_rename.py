import os
import random
from random import randrange
import datetime


path= "static/demo/"
os.chdir(path)

files= os.listdir(".")


def random_date(start):
    current = start
    curr = current + datetime.timedelta(minutes=randrange(60))
    return curr

startDate = datetime.time(13,00,20)


for file in files:
    # x= random_date(startDate)
    # print(type(x))
    x= random.randint(00,59)
    part1= file.split('_')[0]
    os.rename(file, part1+'_'+"2019-10-02 10:{}:25".format("%02d" % x)+".png")
