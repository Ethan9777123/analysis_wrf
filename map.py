import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# GADM Level 3 を読み込む（市区町村レベル）
gdf = gpd.read_file("./data/map/gadm41_KHM_shp/gadm41_KHM_1.shp")

# wakayama = gdf[gdf['NAME_1'] == 'Wakayama']

# 範囲（[minx, miny, maxx, maxy]）を取得
bounds = gdf.total_bounds
minx, miny, maxx, maxy = bounds

# 余白を少し加える
pad_x = (maxx - minx) * 0.05
pad_y = (maxy - miny) * 0.05



# 地図描画
fig, ax = plt.subplots(figsize=(12, 14),
                       subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([minx - pad_x, maxx + pad_x, miny - pad_y, maxy + pad_y], crs=ccrs.PlateCarree())

# 海岸線など
ax.coastlines(resolution='10m')

# 市区町村境界の描画
ax.add_geometries(gdf.geometry, crs=ccrs.PlateCarree(),
                  edgecolor='gray', facecolor='none', linewidth=0.5)

plt.title("map", fontsize=14)
plt.show()
