import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import math
import config
from utils.tools import get_nest_num, get_latlon_minmax, save_as_png, get_foldername, choice_folders, calc_bounds, get_gsmap_file
from utils.interpolation import interpolation
from utils.get_observation import get_observation
import numpy as np
from datetime import datetime
import geopandas as gpd


# plot setting
cmap = config.cmap
norm = config.norm
fontsize = 15

gdf = gpd.read_file("./data/map/gadm41_KHM_shp/gadm41_KHM_1.shp")


def auto_subplot(graph_num, cols, time, lons_list, lats_list, rains_list, title_list, gsmap=True):

    time_str = str(time)
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    yy = dt.year % 100    # → 22
    mm = f'{dt.month:02d}'# → 10
    dd = f'{dt.day:02d}'  # → 16
    hh = f'{dt.hour:02d}' # → 03
    

    if gsmap:
        num = graph_num + 1
    else:
        num = graph_num

    rows = math.ceil(num / cols)

    fig, axes = plt.subplots(rows, cols, 
        figsize=(4 * cols + 2, 3.5 * rows + 1), 
        subplot_kw={'projection': ccrs.PlateCarree()}
    )
    
    
    # flatten して1次元リスト化（重要）
    if isinstance(axes, np.ndarray):
        axes = axes.flatten()
    else:
        axes = [axes]


    for i in range(graph_num):

        lat_min, lat_max, lon_min, lon_max = get_latlon_minmax(lats_list[i], lons_list[i])

        colorbar = axes[i].pcolormesh(
            lons_list[i], 
            lats_list[i], 
            rains_list[i], 
            shading='auto', 
            cmap=cmap, 
            norm=norm, 
            transform=ccrs.PlateCarree()
        )
       
        axes[i].add_feature(cfeature.COASTLINE)
        axes[i].add_feature(cfeature.BORDERS, linestyle=':')

        # 地図　詳細
        axes[i].add_geometries(
            gdf.geometry, crs=ccrs.PlateCarree(),edgecolor='black',
            facecolor='none'
        )
        
        axes[i].set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        axes[i].set_title(f'WRF-{title_list[i]}\n{time}', fontsize=fontsize)

        print(f'{i}, {time}, {rains_list[i].shape}')

    if gsmap:
        # ax3 GSMAP
        gs_file_path = get_gsmap_file(yy, mm, dd, hh)
        rain_gs, lat_gs, lon_gs, ds = get_observation(gs_file_path[0], 'test')
        rain_gs_2d= ds['hourlyPrecipRateGC'].values.T 
        lat_gs_2d = ds['Latitude'].values.T 
        lon_gs_2d = ds['Longitude'].values.T

         # main
        mask, gs_rain_on_wrf, lon_wrf, lat_wrf, latlon_minmax = interpolation(lats_list[i], lons_list[i], lat_gs_2d, lon_gs_2d, rain_gs_2d)
        lat_min, lat_max, lon_min, lon_max = latlon_minmax

        colorbar = axes[i+1].pcolormesh(
            lon_wrf, 
            lat_wrf, 
            gs_rain_on_wrf, 
            shading='auto', 
            cmap=cmap, 
            norm=norm, 
            transform=ccrs.PlateCarree()
        )
        
        axes[i+1].add_feature(cfeature.COASTLINE)
        axes[i+1].add_feature(cfeature.BORDERS, linestyle=':')
        axes[i+1].set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        axes[i+1].set_title(f'GSMAP\n{time}', fontsize=fontsize)

        print(f'GSMAP {i+1}, {time}, {gs_rain_on_wrf.shape}')

        

        

    # plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    plt.tight_layout(pad=3)
    fig.subplots_adjust(hspace=0.4)   

    # bar
    fig.colorbar(colorbar, ax=axes, orientation='horizontal',pad=0.01, shrink=0.6, label='Rainfall (mm/hr)')

    return fig, axes


