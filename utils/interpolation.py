import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from get_rain_houry import get_rain_houry
from wrf import getvar, latlon_coords, to_np
from get_observation import get_observation
# import sys
# import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

fontsize = 20

# ================================== data ==================================

# WRF
rain_wrf, lat_wrf, lon_wrf = get_rain_houry('data/wrfout/2022_10_16_18_shikoku', 2)
# WRF 座標（1D化）
points_wrf = np.column_stack((lat_wrf.values.ravel(), lon_wrf.values.ravel()))


# GSMAP
rain_gs, lat_gs, lon_gs, ds = get_observation(['data/gsmap/2022/10/16/GPMMRG_MAP_2210161400_H_L3S_MCN_05A.nc'], 'test')
# GSMAP 転置で (nlat, nlon) に
rain = ds['hourlyPrecipRateGC'].values.T 
lat2d = ds['Latitude'].values.T 
lon2d = ds['Longitude'].values.T 
# GSMaP 座標と値（1D化）
points_gsmap = np.column_stack((lat2d.ravel(), lon2d.ravel()))
values_gsmap = rain.ravel()

# ==================================  end data ==================================

print(lat_wrf)
print(lon_wrf)
print(rain_wrf)


# ==================================   ==================================

fig, axes = plt.subplots(2, 1, figsize=(12, 14), subplot_kw={'projection': ccrs.PlateCarree()})

# area
lat_min, lat_max = float(lat_wrf.min().values), float(lat_wrf.max().values)
lon_min, lon_max = float(lon_wrf.min().values), float(lon_wrf.max().values)
mask = (
    (lat2d >= lat_min) & (lat2d <= lat_max) &
    (lon2d >= lon_min) & (lon2d <= lon_max)
)



# ================================== nearest neighbor search ==================================
tree = KDTree(points_gsmap)
_, idx = tree.query(points_wrf)

# WRF グリッドに合わせて値を並べ替え
interpolated = values_gsmap[idx].reshape(lat_wrf.shape)
# ==================================  end nearest neighbor search ==================================


# ax1 GSMAP(LEFT)
ax1 = axes[0]

# 降水量データをマスク（範囲外はNaN）
rain_japan = np.where(mask, rain, np.nan)
cf1 = ax1.pcolormesh(lon_wrf, lat_wrf, rain_wrf[14][1], shading='auto', cmap='Blues', transform=ccrs.PlateCarree())
ax1.add_feature(cfeature.COASTLINE)
ax1.add_feature(cfeature.BORDERS, linestyle=':')
ax1.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
ax1.set_title('GSMaP Hourly Precipitation (Japan)', fontsize=fontsize)




# --- 右：WRFグリッド上の降水 ---
ax2 = axes[1]


cf2 = ax2.pcolormesh(lon_wrf, lat_wrf, interpolated, shading='auto', cmap='Blues', transform=ccrs.PlateCarree())
ax2.add_feature(cfeature.COASTLINE)
ax2.add_feature(cfeature.BORDERS, linestyle=':')
ax2.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
ax2.set_title('WRF Precipitation (Japan)', fontsize=fontsize)

fig.colorbar(cf2, ax=axes, orientation='horizontal', shrink=0.6, label='Rainfall (mm/hr)')

# # カラーバー（右）
# plt.colorbar(cf2, ax=ax2, orientation='vertical', label='Rainfall (mm/hr)')


plt.show()





