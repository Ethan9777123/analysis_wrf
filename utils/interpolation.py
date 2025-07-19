import numpy as np
from scipy.spatial import KDTree
from utils.tools import get_latlon_minmax


def interpolation(lat_wrf, lon_wrf, lat_gs_2d, lon_gs_2d, rain_gs_2d):

    if hasattr(lat_wrf, 'values'):
        lat_value = lat_wrf.values.ravel()
    else:
        lat_value = lat_wrf.ravel()
    if hasattr(lon_wrf, 'values'):
        lon_value = lon_wrf.values.ravel()
    else:
        lon_value = lon_wrf.ravel()
    

    # WRF coordinates converted to 1D
    points_wrf = np.column_stack((lat_value, lon_value))

    # GSMaP coordinates converted to 1D
    points_gsmap = np.column_stack((lat_gs_2d.ravel(), lon_gs_2d.ravel()))

    # GSMaP rain converted to 1D
    values_gsmap = rain_gs_2d.ravel()

    # Get WRF Area
    lat_min, lat_max, lon_min, lon_max = get_latlon_minmax(lat_wrf, lon_wrf)
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









