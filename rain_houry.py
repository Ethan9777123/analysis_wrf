import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import getvar, latlon_coords, to_np
import numpy as np
import cartopy.crs as ccrs
from utils.tools import save_as_png, get_wrfoutfiles
import cartopy.feature as cfeature
from pandas import to_datetime
from utils.get_rain_houry import get_rain_houry
import config
from datetime import datetime

def rain_houry(WRFOUT_FOLDERPATH, SAVE_IMAGE_PATH, nest_num=1):


   
    # plot setting
    cmap = config.cmap
    norm = config.norm
    fontsize = 20

    # np setting
    np.set_printoptions(threshold=np.inf)

    # get rain lat lon
    time_rain_wrf, lat, lon = get_rain_houry(WRFOUT_FOLDERPATH, nest_num)

    

    


    # plot
    for i in range(len(time_rain_wrf)):
        
        time_str = str(time_rain_wrf[i][0])
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

        yy = dt.year % 100    # → 22
        mm = f'{dt.month:02d}'# → 10
        dd = f'{dt.day:02d}'  # → 16
        hh = f'{dt.hour:02d}' # → 03

        plt.figure(figsize=(10, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())

        mesh = ax.pcolormesh(
            lon, lat, time_rain_wrf[i][1],
            cmap=cmap,
            norm=norm,   
            shading='auto',
            transform=ccrs.PlateCarree()
        )
        # cf = ax.contourf(
        #     lon_2d, lat_2d, rain_2d,
        #     levels=levels,
        #     cmap=cmap, norm=norm, extend='max'
        # )
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)
        ax.set_title(f'WRF-{time_str}', fontsize=fontsize)
        plt.colorbar(mesh, ax=ax, label="mm/hr", orientation="vertical", shrink=0.7)

        filename = f'wrf_d0{nest_num}_20{yy}{mm}{dd}{hh}.png'

        print(filename)

        # save as png
        save_as_png(plt, filename, SAVE_IMAGE_PATH=SAVE_IMAGE_PATH)







