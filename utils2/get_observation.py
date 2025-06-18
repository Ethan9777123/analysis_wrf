import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from scipy.interpolate import griddata

def get_observation(nc_filename=None, visualize=False):

    nc_filename = 'data/2018_10_23/GPMMRG_MAP_1810230000_H_L3S_MCN_05A.nc'

    ds = xr.open_dataset(nc_filename)

    rain = ds['hourlyPrecipRateGC']  # mm/hr
    lat = ds['Latitude']
    lon = ds['Longitude']

    # print(rain.shape)

    

    if visualize:
        # --- プロット設定 ---
        plt.figure(figsize=(12, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())

        # 地図の範囲を必要に応じて調整（例: 東南アジア）
        ax.set_extent([90, 130, 5, 25], crs=ccrs.PlateCarree())

        # --- 降水量のカラーレンジ指定 (1〜10mm/hr を強調) ---
        mesh = ax.pcolormesh(
            lon, lat, rain,
            cmap='Blues',           # 色設定（他に 'YlGnBu', 'jet', 'viridis' なども可）
            shading='auto',
            vmin=1, vmax=10,        # ここがポイント
            transform=ccrs.PlateCarree()
        )

        # 地図要素追加
        ax.coastlines(resolution='10m')
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.LAND, facecolor='lightgray')
        ax.add_feature(cfeature.OCEAN, facecolor='white')

        # カラーバーなど
        plt.colorbar(mesh, ax=ax, orientation='vertical', label='Rainfall (mm/hr)')
        plt.title("GSMaP Hourly Rainfall")
        plt.tight_layout()
        plt.show()
    
    return rain, lat, lon

