import os
import config
from utils2 import get_nest_num, choice_elem
from rain_houry import rain_houry
from wind_speed import wind_speed
from temp import temp

WRFOUT_FOLDER = config.WRFOUT_FOLDER
IMAGE_FOLDERPATH = config.SAVE_IMAGE_PATH
WRFOUT_FOLDERNAME = config.WRFOUT_FOLDERNAME

WRFOUT_FOLDERPATH = os.path.join(WRFOUT_FOLDER, WRFOUT_FOLDERNAME)

# nest num list
nest_num_list = get_nest_num(WRFOUT_FOLDERPATH=WRFOUT_FOLDERPATH)


elemlist = choice_elem()


for elem in elemlist:
    elem = str(elem)

    if not elem in ['rain', 'wind', 'temp']:
        raise TypeError('input correct elem')
    
    
    if (elem == 'rain'):
        # ---------rain---------
        image_foldername = config.WRFOUT_FOLDERNAME + '_' + 'rain'
        SAVE_IMAGE_PATH = os.path.join(IMAGE_FOLDERPATH, image_foldername)


        for nest_num in nest_num_list:
            rain_houry(WRFOUT_FOLDERPATH=WRFOUT_FOLDERPATH, SAVE_IMAGE_PATH=SAVE_IMAGE_PATH, nest_num=nest_num)

    elif (elem == 'wind'):
        # ---------wind---------
        image_foldername = config.WRFOUT_FOLDERNAME + '_' + 'wind'
        SAVE_IMAGE_PATH = os.path.join(IMAGE_FOLDERPATH, image_foldername)

        for nest_num in nest_num_list:
            wind_speed(WRFOUT_FOLDERPATH=WRFOUT_FOLDERPATH, SAVE_IMAGE_PATH=SAVE_IMAGE_PATH, nest_num=nest_num)

    elif (elem == 'temp'):
        # ---------temp---------
        image_foldername = config.WRFOUT_FOLDERNAME + '_' + '2m_temp'
        SAVE_IMAGE_PATH = os.path.join(IMAGE_FOLDERPATH, image_foldername)

        for nest_num in nest_num_list:
            temp(WRFOUT_FOLDERPATH=WRFOUT_FOLDERPATH, SAVE_IMAGE_PATH=SAVE_IMAGE_PATH, nest_num=nest_num)




