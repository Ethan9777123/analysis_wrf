from utils import make_rain_houry
import os
import config
import numpy as np

from utils2.get_observation import get_observation
import xarray as xr
import numpy as np
from wrf import getvar, interplevel, to_xy_coords, latlon_coords, ll_to_xy
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

import cartopy.crs as ccrs
import cartopy.feature as cfeature


WRFOUT_FOLDER = config.WRFOUT_FOLDER
IMAGE_FOLDERPATH = config.SAVE_IMAGE_PATH
WRFOUT_FOLDERNAME = config.WRFOUT_FOLDERNAME

WRFOUT_FOLDERPATH = os.path.join(WRFOUT_FOLDER, WRFOUT_FOLDERNAME)

rain = make_rain_houry(WRFOUT_FOLDERPATH, nest_num=1)




for timestamp, rain_data in rain.items():

    rain_g, lat_g, lon_g = get_observation()
    lat_wrf, lon_wrf = latlon_coords(rain_data)
    

    
    lat_wrf_min = np.min(lat_wrf.values)
    lat_wrf_max = np.max(lat_wrf.values)
    lon_wrf_min = np.min(lon_wrf.values)
    lon_wrf_max = np.max(lon_wrf.values)

    # debug 1 最小値・最大値の表示
    print("Latitude min:", lat_wrf_min, "max:", lat_wrf_max)
    print("Longitude min:", lon_wrf_min, "max:", lon_wrf_max)

    # GSMaPから切り出し
    # 条件マスクを作成
    mask = (lat_g >= lat_wrf_min) & (lat_g <= lat_wrf_max) & (lon_g >= lon_wrf_min) & (lon_g <= lon_wrf_max)

    # 条件に一致する領域をマスク
    rain_gsmap_cut = rain_g.where(mask, drop=True)

    # 確認（サイズと範囲）
    lat_g = rain_gsmap_cut['Latitude'].values
    lon_g = rain_gsmap_cut['Longitude'].values

    print(rain_g)

    # # debug 2
    # print(rain_gsmap_cut.shape)
    # print("Lat range:", rain_gsmap_cut['Latitude'].min().values, "~", rain_gsmap_cut['Latitude'].max().values)
    # print("Lon range:", rain_gsmap_cut['Longitude'].min().values, "~", rain_gsmap_cut['Longitude'].max().values)

    plt.figure(figsize=(10, 8))

    # 地図の投影法（PlateCarree は経緯度そのまま）
    ax = plt.axes(projection=ccrs.PlateCarree())

    # 降水量のコンター表示
    cf = ax.contourf(
        lon_g, lat_g, rain_gsmap_cut,
        transform=ccrs.PlateCarree(),
        cmap='Blues'
    )

    # 海岸線、国境、河川などを追加
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.RIVERS)

    lat_min, lat_max, lon_min, lon_max = np.round(lat_wrf_min, 1), np.round(lat_wrf_max, 1), np.round(lon_wrf_min, 1), np.round(lon_wrf_max, 1), 

    # 軸の範囲をWRFドメインに合わせて設定
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    # カラーバー追加
    plt.colorbar(cf, orientation='vertical', label='Rainfall (mm)')
    plt.title("GSMaP Rainfall over WRF Domain")
    plt.tight_layout()
    plt.show()

    break