import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from utils.tools import save_as_png, split_by_n
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config



def get_observation(nc_filename, GSMAP_FOLDERNAME, visualize=False, make_png=False):

    # nc_filename = 'data/gsmap/2018/08/29/GPMMRG_MAP_2008290700_H_L3S_MCN_04G.nc'
    print('nc_filename : ', nc_filename)
    ds = xr.open_dataset(nc_filename[0], engine="netcdf4")

    rain = ds['hourlyPrecipRateGC']  # mm/hr
    lat = ds['Latitude']
    lon = ds['Longitude']

    # plot setting
    cmap = config.cmap
    norm = config.norm
    levels = config.levels

    

    if visualize or make_png:
        # --- プロット設定 ---
        plt.figure(figsize=(10, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())

        # 地図の範囲を必要に応じて調整（例: 東南アジア）
        ax.set_extent(config.lat_lon, crs=ccrs.PlateCarree())

        mesh = ax.pcolormesh(
            lon, lat, rain,
            cmap=cmap,
            norm=norm,   
            shading='auto',
            transform=ccrs.PlateCarree()
        )

        # 地図要素追加
        ax.coastlines(resolution='10m')
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.LAND, facecolor='lightgray')
        ax.add_feature(cfeature.OCEAN, facecolor='white')

        # title and file name
        filename = os.path.basename(nc_filename[0])
        timestamp = filename.split('_')[2]
        yy, mm, dd, hh, mi = split_by_n(timestamp, n=2)
        title = f'20{yy}-{mm}-{dd} {hh}:{mi}'
        filename = f'20{yy}_{mm}_{dd}_{hh}'
        # print(yy, mm, dd, hh)

        # カラーバーなど
        plt.colorbar(mesh, ax=ax, orientation='vertical', label=f'rain houry (mm/hr)')
        plt.title(f'rain {title}')
        plt.tight_layout()

        if visualize:
            plt.show()

        if make_png:
            filename = filename + '.png'
            print(filename)
            save_as_png(plt, filename=filename, SAVE_IMAGE_PATH=f'data/gsmap/images/{GSMAP_FOLDERNAME}')

        
        
    
    return rain, lat, lon, ds

# get_observation(nc_filename=None, visualize=True)

