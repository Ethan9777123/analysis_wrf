import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import getvar, latlon_coords, to_np, ALL_TIMES
import numpy as np
import cartopy.crs as ccrs
from glob import glob
import xarray as xr
from utils import get_filepath, save_as_png
import cartopy.feature as cfeature
from pandas import to_datetime
import config
import os

def temp(WRFOUT_FOLDERPATH, SAVE_IMAGE_PATH, nest_num=1):


    # np setting
    np.set_printoptions(threshold=np.inf)


    # get rain info as list
    t2_list = []
    time_list = []
    lat_list = []
    lon_list = []


    # get file list
    filelist = sorted(glob(f'{WRFOUT_FOLDERPATH}/wrfout_d0{nest_num}_*'))


    for f in filelist:
        ncfile = Dataset(f)
        t2 = getvar(ncfile, "T2", timeidx=0)
        t2_list.append(t2)

        # 時間取得（decode 不要）
        times = getvar(ncfile, "times", timeidx=0)
        t1_dt = to_datetime(times.values)  # numpy.datetime64 型も対応
        time_list.append(t1_dt.strftime("%Y%m%d_%H%M"))

        # 緯度経度取得
        lats, lons = latlon_coords(t2)
        lat_list.append(to_np(lats))
        lon_list.append(to_np(lons))

    # make png
    for i in range(len(filelist)):
        t2_2d = to_np(t2_list[i]) - 273.15
        lat_2d = lat_list[i]
        lon_2d = lon_list[i]

        plt.figure(figsize=(10, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())

        contour = plt.contourf(
                    to_np(lon_2d), to_np(lat_2d), t2_2d,
                    levels=range(0, 45, 1), cmap="RdYlBu_r", extend='both'
                )
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)
        ax.set_title(f"2m_temp_{time_list[i]}")
        cbar = plt.colorbar(contour, orientation="horizontal", pad=0.05)
        cbar.set_label("Temperature (°C)")

        filename = f't2_d0{nest_num}_{time_list[i]}.png'

        print(filename)

        save_as_png(plt, filename, SAVE_IMAGE_PATH=SAVE_IMAGE_PATH)