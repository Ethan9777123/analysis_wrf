import os
import questionary
from questionary import Choice
from pathlib import Path
import re
from netCDF4 import Dataset
from wrf import getvar, latlon_coords, to_np, ALL_TIMES
from glob import glob
from pandas import to_datetime

def refine_filename(WRFOUT_FOLDERPATH, old_str=['%3A', ''], new_str='_'):

    
    for filename in os.listdir(WRFOUT_FOLDERPATH):
        for char in old_str:
            if char in filename:
                new_filename = filename.replace(char, new_str)
                old_path = os.path.join(WRFOUT_FOLDERPATH, filename)
                new_path = os.path.join(WRFOUT_FOLDERPATH, new_filename)
                os.rename(old_path, new_path)

def get_filepath(WRFOUT_FOLDERPATH):
    
    refine_filename(WRFOUT_FOLDERPATH)

    filepaths = []

    for filename in os.listdir(WRFOUT_FOLDERPATH):
        filepath = WRFOUT_FOLDERPATH + '/' + filename
        filepaths.append(filepath)
    
    return filepaths

def save_as_png(plt, filename, SAVE_IMAGE_PATH):

    os.makedirs(SAVE_IMAGE_PATH, exist_ok=True)
    save_path = os.path.join(SAVE_IMAGE_PATH, filename)

    plt.savefig(save_path, dpi=300)

def get_nest_num(WRFOUT_FOLDERPATH):

    print(WRFOUT_FOLDERPATH)
    nest_num_list = [1]

    for filename in os.listdir(WRFOUT_FOLDERPATH):
        
        current_nest_num = int(get_word_after_keyword(filename, keyword='d'))
        if (current_nest_num != nest_num_list[-1]):
            nest_num_list.append(current_nest_num)

    return nest_num_list
    
def choice_elem():

    choice_list = [
        Choice("rain"),
        Choice("temp"),
        Choice("wind")
    ]

    elem_list = questionary.checkbox(
        "chose element for analyis", choices=choice_list
    ).ask()

    print(elem_list)

    return elem_list

def choice_folders(folderlist):

    selected = questionary.checkbox(
        "chose image folders for making gif", choices=folderlist
    ).ask()

    

    return selected

def get_foldername(path='./images'):

    target_dir = Path(path)

    subfolders = [f for f in target_dir.iterdir() if f.is_dir()]
    
    # sort
    sorted_subfolders = sorted(subfolders, key=lambda f: f.stat().st_ctime, reverse=True)

    # change to str
    sorted_paths = [str(f) for f in sorted_subfolders]

    return sorted_paths

def get_imagepaths(folderpath, nestnum):

    filepaths = []
    for filename in os.listdir(folderpath):
        filepath = os.path.join(folderpath, filename)
        filepaths.append(filepath)
    
    keyword = 'd0' + str(nestnum)

    matched_files = [f for f in filepaths if keyword in str(f)]

    return matched_files

def get_word_after_keyword(text, keyword='d'):
    
    keyword = str(keyword)
    match = re.search(rf'd(\{keyword}+)', text)
    if match:
        # '01' → int変換で '1' に
        return int(match.group(1))
    else:
        return None
    

def get_rain(WRFOUT_FILEPATH):

    ncfile = Dataset(WRFOUT_FILEPATH)
    rainc = getvar(ncfile, "RAINC", timeidx=0)
    rainnc = getvar(ncfile, "RAINNC", timeidx=0)
    rain_total = rainc + rainnc

    return rain_total

def make_rain_houry(WRFOUT_FOLDERPATH, nest_num=1):

    # get file list
    filelist = sorted(glob(f'{WRFOUT_FOLDERPATH}/wrfout_d0{nest_num}_*'))

    
    pre_rain_total = None
    pre_time = None
    rain_houry = {}
    for f in filelist:
        ncfile = Dataset(f)
        rainc = getvar(ncfile, "RAINC", timeidx=0)
        rainnc = getvar(ncfile, "RAINNC", timeidx=0)
        rain_total = rainc + rainnc

        time = getvar(ncfile, 'times', timeidx=0)
        time = to_datetime(time.values)

        if pre_rain_total is not None:
            rain_houry[pre_time] = rain_total - pre_rain_total

        pre_rain_total = rain_total
        pre_time = time

    return rain_houry

      
    
    