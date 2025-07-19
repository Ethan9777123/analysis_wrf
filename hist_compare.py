
from utils.tools import get_nest_num, get_latlon_minmax, save_as_png, get_foldername, choice_folders, calc_bounds, get_gsmap_file
from utils.get_rain_houry import get_rain_houry
from datetime import datetime
from utils.auto_subplot import auto_subplot
from utils.rain_histogram import rain_histogram
import config
import os
import matplotlib.pyplot as plt
import numpy as np


# get folders
folders = get_foldername('./data/wrfout')
choices = choice_folders(folders)

folders_num = len(choices)

for i in range(len(choices)):
    print(f'{i} : {choices[i]}')

# nest num
nest_num_list = get_nest_num(choices[0])



for nest_num in nest_num_list:

    dict_list = []
    title_list = []
    rains_list = []
    lats_list = []
    lons_list = []

    for num in range(folders_num):
        time_rains, lats, lons = get_rain_houry(choices[num], nest_num)
        dict_list.append(dict(time_rains))
        
        title_list.append(os.path.basename(choices[num])[-4:])
        lats_list.append(lats)
        lons_list.append(lons)
        rains_list.append(time_rains[:][1])
        


    for i in range(len(time_rains)):

        rain_list_one_time = []
        lat_list_one_time = []
        lon_list_one_time = []

    

        # time
        time = time_rains[i][0]
        
        time_str = str(time)
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        yy = dt.year % 100    # → 22
        mm = f'{dt.month:02d}'# → 10
        dd = f'{dt.day:02d}'  # → 16
        hh = f'{dt.hour:02d}' # → 03

        for num in range(folders_num):
            
            rain = dict_list[num].get(time)

            # print('rain', rain)

            if rain is None:
                print(f'not found {time_str} in wrfout {num}')
                break
            
            
            
            lat_list_one_time.append(lats_list[num])
            lon_list_one_time.append(lons_list[num])
            rain_list_one_time.append(rain)

        rain_histogram(
            graph_num=folders_num, 
            lons_list=lon_list_one_time, lats_list=lat_list_one_time,
            time=time, cols=2, 
            rains_list=rain_list_one_time, title_list=title_list
        )

        

        filename = f'd0{nest_num}_20{yy}-{mm}-{dd}-{hh}'
        image_foldername = config.COMPARE_WRF_IMAGE_FOLDERNAME + '_hist'
        SAVE_IMAGE_PATH = os.path.join(config.SAVE_IMAGE_PATH, image_foldername)

        save_as_png(plt, filename, SAVE_IMAGE_PATH)

        