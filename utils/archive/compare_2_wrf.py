import os
import config
from utils.tools import get_nest_num, get_latlon_minmax, save_as_png, get_foldername, choice_folders, calc_bounds, get_gsmap_file
from utils.get_rain_houry import get_rain_houry
from utils.interpolation import interpolation
from utils.get_observation import get_observation
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

# basename
basename_1 = os.path.basename(os.path.normpath(wrfout_folderpath_1))
basename_2 = os.path.basename(os.path.normpath(wrfout_folderpath_2))

# cu_physics setting
wrf_1_cu = basename_1[-4:]
wrf_2_cu = basename_2[-4:]


# nest num list
nest_num_list = get_nest_num(WRFOUT_FOLDERPATH=wrfout_folderpath_1)

add_gsmap = True

for nest_num in nest_num_list:

    # WRF rain, lat, lon
    time_rain_wrf_1, lat_wrf_1, lon_wrf_1 = get_rain_houry(wrfout_folderpath_1, nest_num)
    time_rain_wrf_2, lat_wrf_2, lon_wrf_2 = get_rain_houry(wrfout_folderpath_2, nest_num)

    

    
    for i in range(len(time_rain_wrf_1)):

        
        # time
        time = time_rain_wrf_1[i][0]
        time_str_1 = str(time)
        dt1 = datetime.strptime(time_str_1, "%Y-%m-%d %H:%M:%S")
        yy1 = dt1.year % 100    # → 22
        mm1 = f'{dt1.month:02d}'# → 10
        dd1 = f'{dt1.day:02d}'  # → 16
        hh1 = f'{dt1.hour:02d}' # → 03

        rain_wrf_1 = time_rain_wrf_1[i][1]
        time_rain_wrf_2_dict = dict(time_rain_wrf_2)
        rain_wrf_2 = time_rain_wrf_2_dict.get(time)

       
        # Error handling
        if rain_wrf_2 is None:
            print(f'not found {time_str_1} in wrfout 2')
            break
        
        lat_wrf_1_new = calc_bounds(lat_wrf_1)
        lat_wrf_2_new = calc_bounds(lat_wrf_2)
        lon_wrf_1_new = calc_bounds(lon_wrf_1)
        lon_wrf_2_new = calc_bounds(lon_wrf_2)
        

        # area
        lat_min_1, lat_max_1, lon_min_1, lon_max_1 = get_latlon_minmax(lat_wrf_1_new, lon_wrf_1_new)
        lat_min_2, lat_max_2, lon_min_2, lon_max_2 = get_latlon_minmax(lat_wrf_2_new, lon_wrf_2_new)

        if add_gsmap:
            graph_num = 3
        else:
            graph_num = 2
        
        
        # plot
        fig, axes = plt.subplots(graph_num, 1, figsize=(12, 14), subplot_kw={'projection': ccrs.PlateCarree()})
        fontsize = 20

        # ax1
        ax1 = axes[0]
        cf1 = ax1.pcolormesh(lon_wrf_1_new, lat_wrf_1_new, rain_wrf_1, shading='flat', cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE)
        ax1.add_feature(cfeature.BORDERS, linestyle=':')
        ax1.set_extent([lon_min_1, lon_max_1, lat_min_1, lat_max_1], crs=ccrs.PlateCarree())
        ax1.set_title(f'WRF-{time_str_1}_{wrf_1_cu}', fontsize=fontsize)

        

        # ax2 
        ax2 = axes[1]
        cf2 = ax2.pcolormesh(lon_wrf_2_new, lat_wrf_2_new, rain_wrf_2, shading='flat', cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE)
        ax2.add_feature(cfeature.BORDERS, linestyle=':')
        ax2.set_extent([lon_min_1, lon_max_1, lat_min_1, lat_max_1], crs=ccrs.PlateCarree())
        ax2.set_title(f'WRF-{time_str_1}_{wrf_2_cu}', fontsize=fontsize)

        color_bar = cf2

        if add_gsmap:

            # ax3 GSMAP
            gs_file_path = get_gsmap_file(yy1, mm1, dd1, hh1)
            rain_gs, lat_gs, lon_gs, ds = get_observation(gs_file_path[0], 'test')
            rain_gs_2d= ds['hourlyPrecipRateGC'].values.T 
            lat_gs_2d = ds['Latitude'].values.T 
            lon_gs_2d = ds['Longitude'].values.T
            

            # main
            mask, gs_rain_on_wrf, lon_wrf, lat_wrf, latlon_minmax = interpolation(lat_wrf_1_new, lon_wrf_1_new, lat_gs_2d, lon_gs_2d, rain_gs_2d)
            lat_min, lat_max, lon_min, lon_max = latlon_minmax
            ax3 = axes[2]
            cf3 = ax3.pcolormesh(lon_wrf, lat_wrf, gs_rain_on_wrf, shading='auto', cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
            ax3.add_feature(cfeature.COASTLINE)
            ax3.add_feature(cfeature.BORDERS, linestyle=':')
            ax3.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
            ax3.set_title(f'GSMAP-{time_str_1}', fontsize=fontsize)

            color_bar = cf3

        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        plt.tight_layout()

        # bar
        fig.colorbar(color_bar, ax=axes, orientation='horizontal',pad=0.01, shrink=0.6, label='Rainfall (mm/hr)')

        filename = f'compare_2_wrf_d0{nest_num}_20{yy1}{mm1}{dd1}{hh1}.png'
        image_foldername = 'compare_2_wrf_' + config.WRFOUT_FOLDERNAME 
        SAVE_IMAGE_PATH = os.path.join(IMAGE_FOLDERPATH, image_foldername)

        

        save_as_png(plt, filename, SAVE_IMAGE_PATH)


