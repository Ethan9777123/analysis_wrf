from glob import glob
import os
from PIL import Image
import config
from utils.tools import get_imagepaths, get_nest_num, get_foldername, choice_folders

SAVE_IMAGE_PATH = config.SAVE_IMAGE_PATH

def animation(target_images, filename):


    frames = []

    for img_path in target_images:
        img = Image.open(img_path)
        frames.append(img)

    frames[0].save(
        f'{config.SAVE_GIF_PATH}/{filename}.gif',
        save_all=True,
        append_images=frames[1:],
        duration=200,  # ミリ秒 (500ms = 0.5秒)
        loop=0
    )


# main
if __name__ == '__main__':
    # get folders
    folderpath_list = choice_folders(get_foldername(path=config.SAVE_IMAGE_PATH))

    for folder in folderpath_list:
        nest_num_list = get_nest_num(folder)
        
        for nest_num in nest_num_list:
            
            folder_name = os.path.basename(folder)
            filename = f'{folder_name}_{nest_num}'
            images = get_imagepaths(folderpath=folder, nestnum=nest_num)

            animation(target_images=images, filename=filename)
        

