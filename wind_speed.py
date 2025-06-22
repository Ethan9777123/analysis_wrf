import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import getvar, latlon_coords, to_np
import numpy as np
import cartopy.crs as ccrs
from utils.tools import save_as_png, get_wrfoutfiles
import cartopy.feature as cfeature
from pandas import to_datetime


def wind_speed(WRFOUT_FOLDERPATH, SAVE_IMAGE_PATH, nest_num=1):

    # np setting
    np.set_printoptions(threshold=np.inf)


    # get rain info as list
    u10_list = []
    v10_list = []
    time_list = []
    lat_list = []
    lon_list = []


    # get file list
    filelist = get_wrfoutfiles(wrfout_folderpath=WRFOUT_FOLDERPATH, nest_num=nest_num)



    for f in filelist:
        ncfile = Dataset(f)
        u10 = getvar(ncfile, "U10", timeidx=0)
        v10 = getvar(ncfile, "V10", timeidx=0)

        u10_list.append(u10)
        v10_list.append(v10)

        # 時間取得（decode 不要）
        times = getvar(ncfile, "times", timeidx=0)
        t1_dt = to_datetime(times.values)  # numpy.datetime64 型も対応
        time_list.append(t1_dt.strftime("%Y%m%d_%H%M"))

        # 緯度経度取得
        lats, lons = latlon_coords(u10)
        lat_list.append(to_np(lats))
        lon_list.append(to_np(lons))

    # make png
    for i in range(len(filelist)):
        u10_2d = to_np(u10_list[i])
        v10_2d = to_np(v10_list[i])
        lat_2d = lat_list[i]
        lon_2d = lon_list[i]

        # サブサンプリング（表示を軽くする）
        step = 5
        u10_sub = to_np(u10_2d[::step, ::step])
        v10_sub = to_np(v10_2d[::step, ::step])
        lons_sub = to_np(lon_2d[::step, ::step])
        lats_sub = to_np(lat_2d[::step, ::step])

        wind_speed = np.sqrt(u10_2d**2 + v10_2d**2)

        plt.figure(figsize=(10, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)

        # ベクトル（矢印）
        plt.quiver(lons_sub, lats_sub, u10_sub, v10_sub, color='blue')
        
        plt.title("10m Wind Speed and Direction")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        filename = f'wind_d0{nest_num}_{time_list[i]}.png'
        
        print(filename)
        
        save_as_png(plt, filename, SAVE_IMAGE_PATH=SAVE_IMAGE_PATH)