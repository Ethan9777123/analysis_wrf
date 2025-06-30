import os
import config
from utils.tools import get_nest_num, get_latlon_minmax, save_as_png, get_foldername, choice_folders
from utils.get_rain_houry import get_rain_houry
from datetime import datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


IMAGE_FOLDERPATH = config.SAVE_IMAGE_PATH

# plot setting
cmap = config.cmap
norm = config.norm


# get folder paths
folders = get_foldername('./data/wrfout')
choices = choice_folders(folders)

# Error handling
if (len(choices) != 2):
    raise ValueError('select 2 folders')

# 2 WRFOUT FOLDERPATHS
wrfout_folderpath_1 = choices[0]
wrfout_folderpath_2 = choices[1]

# nest num list
nest_num_list = get_nest_num(WRFOUT_FOLDERPATH=wrfout_folderpath_1)

for nest_num in nest_num_list:

    # WRF rain, lat, lon
    time_rain_wrf_1, lat_wrf_1, lon_wrf_1 = get_rain_houry(wrfout_folderpath_1, nest_num)
    time_rain_wrf_2, lat_wrf_2, lon_wrf_2 = get_rain_houry(wrfout_folderpath_2, nest_num)

    for i in range(len(time_rain_wrf_1)):

        
        time_rain_wrf_2_dict = dict(time_rain_wrf_2)

        # time
        time_str_1 = str(time_rain_wrf_1[i][0])
        dt1 = datetime.strptime(time_str_1, "%Y-%m-%d %H:%M:%S")
        yy1 = dt1.year % 100    # → 22
        mm1 = f'{dt1.month:02d}'# → 10
        dd1 = f'{dt1.day:02d}'  # → 16
        hh1 = f'{dt1.hour:02d}' # → 03

        rain_wrf_1 = time_rain_wrf_1[i][1]
        time_rain_wrf_2_dict = dict(time_rain_wrf_2)
        rain_wrf_2 = time_rain_wrf_2_dict.get(time_str_1)

        # Error handling
        if rain_wrf_2 is None:
            print(f'not found {time_str_1} in wrfout 2')
            break

        

        # area
        lat_min_1, lat_max_1, lon_min_1, lon_max_1 = get_latlon_minmax(lat_wrf_1, lon_wrf_1)
        lat_min_2, lat_max_2, lon_min_2, lon_max_2 = get_latlon_minmax(lat_wrf_2, lon_wrf_2)
        
        
        # plot
        fig, axes = plt.subplots(2, 1, figsize=(12, 14), subplot_kw={'projection': ccrs.PlateCarree()})
        fontsize = 20

        # ax1 WRF(LEFT)
        ax1 = axes[0]
        cf1 = ax1.pcolormesh(lon_wrf_1, lat_wrf_1, rain_wrf_1, shading='auto', cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE)
        ax1.add_feature(cfeature.BORDERS, linestyle=':')
        ax1.set_extent([lon_min_1, lon_max_1, lat_min_1, lat_max_1], crs=ccrs.PlateCarree())
        ax1.set_title(f'WRF-{time_str_1}', fontsize=fontsize)

        

        # ax2 GSMAP(RIGHT)
        ax2 = axes[1]
        cf2 = ax2.pcolormesh(lon_wrf_2, lat_wrf_2, rain_wrf_2, shading='auto', cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE)
        ax2.add_feature(cfeature.BORDERS, linestyle=':')
        ax2.set_extent([lon_min_1, lon_max_1, lat_min_1, lat_max_1], crs=ccrs.PlateCarree())
        ax2.set_title(f'GSMAP-{time_str_1}', fontsize=fontsize)

        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        # bar
        fig.colorbar(cf2, ax=axes, orientation='horizontal',pad=0.01, shrink=0.6, label='Rainfall (mm/hr)')

        filename = f'compare_2_wrf_d0{nest_num}_20{yy1}{mm1}{dd1}{hh1}.png'
        image_foldername = 'compare' + config.WRFOUT_FOLDERNAME 
        SAVE_IMAGE_PATH = os.path.join(IMAGE_FOLDERPATH, image_foldername)

        print(filename)

        save_as_png(plt, filename, SAVE_IMAGE_PATH)


print(choices)