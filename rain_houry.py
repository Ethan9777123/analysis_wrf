import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import getvar, latlon_coords, to_np, ALL_TIMES
import numpy as np
import cartopy.crs as ccrs
from glob import glob
import xarray as xr
from utils2 import get_filepath, save_as_png
import cartopy.feature as cfeature
from pandas import to_datetime
import matplotlib.colors as mcolors
import os
import config

def rain_houry(WRFOUT_FOLDERPATH, SAVE_IMAGE_PATH, nest_num=1):


    bounds = [0, 1, 5, 10, 20, 30, 50, 80, 100]
    colors = ['white', 'lightblue', 'blue', 'lime', 'yellow', 'orange', 'red', 'purple']

    # plot setting
    cmap = mcolors.ListedColormap(colors)
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    levels = [0, 1, 5, 10, 20, 30, 40, 50]


    # np setting
    np.set_printoptions(threshold=np.inf)


    # get lats, lons
    wrf_files = get_filepath(WRFOUT_FOLDERPATH=WRFOUT_FOLDERPATH)
    wrf_file = Dataset(wrf_files[0])
    rainc_2 = getvar(wrf_file, "RAINC", timeidx=0)    # convective
    rainnc_2 = getvar(wrf_file, "RAINNC", timeidx=0)  # non-convective
    rain_total_2 = rainc_2 + rainnc_2
    lats, lons = latlon_coords(rain_total_2)
    lat_2d = to_np(lats)
    lon_2d = to_np(lons)



    # get file list
    filelist = sorted(glob(f'{WRFOUT_FOLDERPATH}/wrfout_d0{nest_num}_*'))

    # get rain info as list
    rain_total_list = []
    time_list = []
    lat_list = []
    lon_list = []

    for f in filelist:
        ncfile = Dataset(f)
        rainc = getvar(ncfile, "RAINC", timeidx=0)
        rainnc = getvar(ncfile, "RAINNC", timeidx=0)
        rain_total = rainc + rainnc
        rain_total_list.append(rain_total)

        # 時間取得（decode 不要）
        times = getvar(ncfile, "times", timeidx=0)
        t1_dt = to_datetime(times.values)  # numpy.datetime64 型も対応
        time_list.append(t1_dt.strftime("%Y%m%d_%H%M"))

        # 緯度経度取得
        lats, lons = latlon_coords(rain_total)
        lat_list.append(to_np(lats))
        lon_list.append(to_np(lons))


    # plot
    for i in range(len(filelist) - 1):
        rain_2d = to_np(rain_total_list[i+1] - rain_total_list[i])
        lat_2d = lat_list[i]
        lon_2d = lon_list[i]

        plt.figure(figsize=(10, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())

        cf = ax.contourf(
            lon_2d, lat_2d, rain_2d,
            levels=levels,
            cmap=cmap, norm=norm, extend='max'
        )
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)
        ax.set_title(f"{time_list[i]} - {time_list[i+1]}")
        plt.colorbar(cf, ax=ax, label="mm/hr", orientation="vertical", shrink=0.7)

        filename = f'rain_d0{nest_num}_{time_list[i]}_{time_list[i+1]}.png'

        print(filename)

        # save as png
        save_as_png(plt, filename, SAVE_IMAGE_PATH=SAVE_IMAGE_PATH)







