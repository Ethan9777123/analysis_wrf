from utils.get_observation import get_observation
from glob import glob
import config
import sys
from utils.tools import generate_hourly_timestamps, download_gsmap
import os
from datetime import datetime



# yy mm dd hh
start_date = sys.argv[1]
end_date = sys.argv[2]

start = datetime.strptime(start_date, "%Y%m%d%H")
end = datetime.strptime(end_date, "%Y%m%d%H")

dt_list = generate_hourly_timestamps(start, end)

current_dir = os.getcwd()
    

for timestamp in dt_list:
    dt = datetime.strptime(timestamp, "%Y%m%d%H")
    yy = dt.strftime("%y")  # "22"
    mm = dt.strftime("%m")  # "06"
    dd = dt.strftime("%d")  # "05"
    hh = dt.strftime("%H")  # "00"

    filename = f'GPMMRG_MAP_{yy}{mm}{dd}{hh}00_H_L3S_MCN_05A.nc'
    store_path = os.path.join(current_dir,'data', 'gsmap', f'20{yy}', f'{mm}', f'{dd}', f'{filename}')
    if not os.path.exists(store_path):
        download_gsmap(timestamp)

    file = glob(store_path)
    get_observation(nc_filename=file, GSMAP_FOLDERNAME=config.GSMAP_FOLDERNAMAE, visualize=False, make_png=True)

