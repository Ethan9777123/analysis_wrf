import numpy as np
from scipy.spatial import KDTree



def interpolation(lat_wrf, lon_wrf, lat_gs_2d, lon_gs_2d, rain_gs_2d):

    # WRF coordinates converted to 1D
    points_wrf = np.column_stack((lat_wrf.values.ravel(), lon_wrf.values.ravel()))

    # GSMaP coordinates converted to 1D
    points_gsmap = np.column_stack((lat_gs_2d.ravel(), lon_gs_2d.ravel()))

    # GSMaP rain converted to 1D
    values_gsmap = rain_gs_2d.ravel()

    # Get WRF Area
    lat_min, lat_max = float(lat_wrf.min().values), float(lat_wrf.max().values)
    lon_min, lon_max = float(lon_wrf.min().values), float(lon_wrf.max().values)
    mask = (
        (lat_gs_2d >= lat_min) & (lat_gs_2d <= lat_max) &
        (lon_gs_2d >= lon_min) & (lon_gs_2d <= lon_max)
    )

    # nearest neighbor search
    tree = KDTree(points_gsmap)
    _, idx = tree.query(points_wrf)

    # Sort values ​​to fit the WRF grid
    gs_rain_on_wrf = values_gsmap[idx].reshape(lat_wrf.shape)


    return mask, gs_rain_on_wrf, lon_wrf, lat_wrf, [lat_min, lat_max, lon_min, lon_max]









