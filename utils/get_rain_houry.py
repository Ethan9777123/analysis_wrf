from netCDF4 import Dataset
from wrf import getvar
from glob import glob
from pandas import to_datetime
from wrf import getvar, latlon_coords, to_np

def get_rain_houry(WRFOUT_FOLDERPATH, nest_num):

    # get file list
    filelist = sorted(glob(f'{WRFOUT_FOLDERPATH}/wrfout_d0{nest_num}_*'))

    

    # main
    pre_rain_total = None
    pre_time = None
    rain_houry = []

    for i in range(len(filelist)):
        ncfile = Dataset(filelist[i])
        rainc = getvar(ncfile, "RAINC", timeidx=0)
        rainnc = getvar(ncfile, "RAINNC", timeidx=0)
        rain_total = rainc + rainnc

        # lat lon
        lat, lon = latlon_coords(rainc)  # shape: (ny, nx)

        time = getvar(ncfile, 'times', timeidx=0)
        time = to_datetime(time.values)

        if pre_rain_total is not None:
            rain_houry.append([pre_time, (rain_total - pre_rain_total)])

        pre_rain_total = rain_total
        pre_time = time

    
    return rain_houry, lat, lon