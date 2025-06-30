import matplotlib.colors as mcolors


WRFOUT_FOLDERNAME = '2020_10_14_16_cambodia_cu_0'

GSMAP_FOLDERNAMAE = '2020_10_14_16_cambodia_cu_0'

SAVE_IMAGE_PATH = f'./data/images'
SAVE_GSMAP_IMAGE_PATH = f'./data/gsmap/images'
SAVE_GIF_PATH = f'./data/gif'
WRFOUT_FOLDER = f'./data/wrfout'

# lat lon
cambodia_lat_lon = [98, 112, 8, 17]
japan_lat_lon = [122, 154, 24, 46]


lat_lon = japan_lat_lon



# matplot setting
bounds = [0, 1, 5, 10, 20, 30, 50, 80, 100]
colors = ['white', 'lightblue', 'blue', 'lime', 'yellow', 'orange', 'red', 'purple']
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(bounds, cmap.N)
levels = [0, 1, 5, 10, 20, 30, 40, 50]