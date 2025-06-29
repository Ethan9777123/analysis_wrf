import os
import config
from utils.tools import get_nest_num, get_gsmap_file, save_as_png
from utils.get_rain_houry import get_rain_houry
from utils.get_observation import get_observation
from utils.interpolation import interpolation
from datetime import datetime

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

WRFOUT_FOLDER = config.WRFOUT_FOLDER
IMAGE_FOLDERPATH = config.SAVE_IMAGE_PATH
WRFOUT_FOLDERNAME = config.WRFOUT_FOLDERNAME

# plot setting
cmap = config.cmap
norm = config.norm


# ======================== data ======================== 
WRFOUT_FOLDERPATH = os.path.join(WRFOUT_FOLDER, WRFOUT_FOLDERNAME)

# nest num list
nest_num_list = get_nest_num(WRFOUT_FOLDERPATH=WRFOUT_FOLDERPATH)
image_foldername = 'compare' + config.WRFOUT_FOLDERNAME 
SAVE_IMAGE_PATH = os.path.join(IMAGE_FOLDERPATH, image_foldername)

for nest_num in nest_num_list:
    
    # WRF rain, lat, lon
    rain_wrf, lat_wrf, lon_wrf = get_rain_houry(WRFOUT_FOLDERPATH, nest_num)

    for i in range(len(rain_wrf)):
        time_str = str(rain_wrf[i][0])
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

        yy = dt.year % 100    # → 22
        mm = f'{dt.month:02d}'         # → 10
        dd = f'{dt.day:02d}'           # → 16
        hh = f'{dt.hour:02d}' # → 03

        # gsmap
        gs_file_path = get_gsmap_file(yy, mm, dd, hh)
        rain_gs, lat_gs, lon_gs, ds = get_observation(gs_file_path[0], 'test')
        
        # GSMAP 転置で (nlat, nlon) に
        rain_gs_2d= ds['hourlyPrecipRateGC'].values.T 
        lat_gs_2d = ds['Latitude'].values.T 
        lon_gs_2d = ds['Longitude'].values.T

        # main
        mask, gs_rain_on_wrf, lon_wrf, lat_wrf, latlon_minmax = interpolation(lat_wrf, lon_wrf, lat_gs_2d, lon_gs_2d, rain_gs_2d)

        # area
        lat_min, lat_max, lon_min, lon_max = latlon_minmax

        # plot
        fig, axes = plt.subplots(2, 1, figsize=(12, 14), subplot_kw={'projection': ccrs.PlateCarree()})
        fontsize = 20

        # ax1 WRF(LEFT)
        ax1 = axes[0]
        cf1 = ax1.pcolormesh(lon_wrf, lat_wrf, rain_wrf[i][1], shading='auto', cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE)
        ax1.add_feature(cfeature.BORDERS, linestyle=':')
        ax1.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        ax1.set_title(f'WRF-{time_str}', fontsize=fontsize)

        

        # ax2 GSMAP(RIGHT)
        ax2 = axes[1]
        cf2 = ax2.pcolormesh(lon_wrf, lat_wrf, gs_rain_on_wrf, shading='auto', cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE)
        ax2.add_feature(cfeature.BORDERS, linestyle=':')
        ax2.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        ax2.set_title(f'GSMAP-{time_str}', fontsize=fontsize)

        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        # bar
        fig.colorbar(cf2, ax=axes, orientation='horizontal',pad=0.01, shrink=0.6, label='Rainfall (mm/hr)')

        filename = f'compare_d0{nest_num}_20{yy}{mm}{dd}{hh}.png'
        image_foldername = 'compare' + config.WRFOUT_FOLDERNAME 
        SAVE_IMAGE_PATH = os.path.join(IMAGE_FOLDERPATH, image_foldername)

        print(filename)

        save_as_png(plt, filename, SAVE_IMAGE_PATH)
   

