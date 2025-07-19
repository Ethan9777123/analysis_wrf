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


# plot setting
cmap = config.cmap
norm = config.norm
bins = [0.1, 0.2,0.3, 0.5, 1, 2, 3, 4, 5, 10, 20, 30, 50, 100]
fontsize = 15

# === カラーパレット（各グラフの色）===
colors = ['skyblue', 'lightcoral', 'lightgreen', 'plum']
labels = [f'{bins[i]}-{bins[i+1]} mm' for i in range(len(bins)-1)]

def rain_histogram(graph_num, lons_list, lats_list, time, cols, rains_list, title_list, gsmap=True):

    time_str = str(time)
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    yy = dt.year % 100    # → 22
    mm = f'{dt.month:02d}'# → 10
    dd = f'{dt.day:02d}'  # → 16
    hh = f'{dt.hour:02d}' # → 03
    rows = math.ceil(graph_num / cols)

    fig, axes = plt.subplots(rows, cols, 
        figsize=(4 * cols + 2, 3.5 * rows + 1)
    )
    
    
    
    # flatten して1次元リスト化（重要）
    if isinstance(axes, np.ndarray):
        axes = axes.flatten()
    else:
        axes = [axes]

    # get y max
    y_max = 0
    for i in range(graph_num):
        rain_flat = rains_list[i].values.flatten()
        rain_flat = rain_flat[~np.isnan(rain_flat)]  # NaN除去
        counts, _ = np.histogram(rain_flat, bins=bins)

        # max y
        y_max_current = counts.max()
        if (y_max_current > y_max):
            y_max = y_max_current


    for i in range(graph_num):

        rain_flat = rains_list[i].values.flatten()
        rain_flat = rain_flat[~np.isnan(rain_flat)]  # NaN除去

        # ヒストグラム集計
        counts, _ = np.histogram(rain_flat, bins=bins)


        # === 5. 棒グラフ描画 ===
        axes[i].bar(labels, counts, color=colors[i % len(colors)], alpha=0.7, edgecolor='black')
        axes[i].set_title(f'WRF\n{title_list[i]}-{time}')
        axes[i].set_xticklabels(labels, rotation=45)
        axes[i].set_ylim(0, y_max + 10)
        if i == 0:
            axes[i].set_ylabel('points num')

    if gsmap:
        # ax3 GSMAP
        gs_file_path = get_gsmap_file(yy, mm, dd, hh)
        rain_gs, lat_gs, lon_gs, ds = get_observation(gs_file_path[0], 'test')
        rain_gs_2d= ds['hourlyPrecipRateGC'].values.T 
        lat_gs_2d = ds['Latitude'].values.T 
        lon_gs_2d = ds['Longitude'].values.T

         # main
        mask, gs_rain_on_wrf, lon_wrf, lat_wrf, latlon_minmax = interpolation(
            lats_list[i], lons_list[i], lat_gs_2d, lon_gs_2d, rain_gs_2d
        )

        rain_flat = gs_rain_on_wrf.flatten()
        rain_flat = rain_flat[~np.isnan(rain_flat)]  # NaN除去

        # ヒストグラム集計
        counts, _ = np.histogram(rain_flat, bins=bins)

        # === 5. 棒グラフ描画 ===
        axes[i+1].bar(labels, counts, color=colors[i % len(colors)], alpha=0.7, edgecolor='black')
        axes[i+1].set_title(f'GSMAP\n{time}')
        axes[i+1].set_xticklabels(labels, rotation=45)
        axes[i+1].set_ylim(0, y_max + 10)
        if i == 0:
            axes[i+1].set_ylabel('points num')

        

        

    # plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    plt.tight_layout(pad=3)
    fig.subplots_adjust(hspace=0.4)   

    return fig, axes