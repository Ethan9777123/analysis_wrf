from glob import glob
import os
from PIL import Image
import config

def animation(foldername, nestnum=1, target='d0',  folderpath='./images'):

    target = target + str(nestnum) + '*'

    filepath = os.path.join(folderpath, foldername, target)

    target_imgs = glob(filepath)

    print(target_imgs)

    frames = []

    for img_path in target_imgs:
        img = Image.open(img_path)
        frames.append(img)

    frames[0].save(
        f'{foldername}_{nestnum}.gif',
        save_all=True,
        append_images=frames[1:],
        duration=200,  # ミリ秒 (500ms = 0.5秒)
        loop=0
    )

nestnum = config.nest_num

WRF_OUT_FOLDERNAME = config.WRF_OUT_FOLDERNAME
element = config.element
IMAGE_FOLDERNAME = WRF_OUT_FOLDERNAME + '_' + element
SAVE_IMAGE_PATH = f'./wrf_images/{IMAGE_FOLDERNAME}'

if element == 'rain':
    target = f'rain_d0'
elif element == 'wind':
    target = f'wind_d0'
elif element == '2m_temp':
    target = f't2_d0'


animation(IMAGE_FOLDERNAME, target=target, nestnum=nestnum)