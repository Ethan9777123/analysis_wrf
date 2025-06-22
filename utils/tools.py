import os
import questionary
from questionary import Choice
from pathlib import Path
import re
from netCDF4 import Dataset
from wrf import getvar
from glob import glob
from pandas import to_datetime
from datetime import timedelta
import paramiko
from dotenv import load_dotenv
from datetime import datetime

def refine_filename(WRFOUT_FOLDERPATH, old_str=['%3A', ''], new_str='_'):

    
    for filename in os.listdir(WRFOUT_FOLDERPATH):
        for char in old_str:
            if char in filename:
                new_filename = filename.replace(char, new_str)
                old_path = os.path.join(WRFOUT_FOLDERPATH, filename)
                new_path = os.path.join(WRFOUT_FOLDERPATH, new_filename)
                os.rename(old_path, new_path)

def get_filepath(folderpath):
    
    refine_filename(folderpath)

    filepaths = []

    for filename in os.listdir(folderpath):
        filepath = folderpath + '/' + filename
        filepaths.append(filepath)
    
    return filepaths.sort()

def get_wrfoutfiles(wrfout_folderpath, nest_num=1):

    refine_filename(WRFOUT_FOLDERPATH=wrfout_folderpath)
    
    filelist = sorted(glob(f'{wrfout_folderpath}/wrfout_d0{nest_num}_*'))

    return filelist

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

      
def split_by_n(s, n=2):
    return [s[i:i+n] for i in range(0, len(s), n)]

def generate_hourly_timestamps(start, end):

    dt_list = []
    current = start
    while current <= end:
        dt_list.append(current.strftime("%Y%m%d%H"))  # 文字列で格納
        current += timedelta(hours=1)

    return dt_list

def download_gsmap(timestamp):

    # read .env
    load_dotenv()

    # conf
    host = 'ftp.gportal.jaxa.jp'
    port = 2051

    username = os.getenv("G_PORTAL_USERNAME")
    password = os.getenv("G_PORTAL_PASSWORD")

    dt = datetime.strptime(timestamp, "%Y%m%d%H")
    yy = dt.strftime("%y")  # "22"
    mm = dt.strftime("%m")  # "06"
    dd = dt.strftime("%d")  # "05"
    hh = dt.strftime("%H")  # "00"

    # dir
    filename = f'GPMMRG_MAP_{yy}{mm}{dd}{hh}00_H_L3S_MCN_05A.nc'
    path = f'/standard/GSMaP/3.GSMAP.H/05A/20{yy}/{mm}/{dd}/{filename}'
    current_dir = os.getcwd()
    store_path = os.path.join(current_dir,'data', 'gsmap', f'20{yy}', f'{mm}', f'{dd}', f'{filename}')

    # ✅ 保存先ディレクトリが無ければ作成
    os.makedirs(os.path.dirname(store_path), exist_ok=True)

    # SFTP接続
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(path, store_path)  # ダウンロード
    sftp.close()

    print("✅ ダウンロード完了:", filename)