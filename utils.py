import os
import questionary
from questionary import Choice

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

    print('get_nest_num : ', WRFOUT_FOLDERPATH)
    nest_num_list = [1]

    for filename in os.listdir(WRFOUT_FOLDERPATH):
        print(filename)
        current_nest_num = int(filename[9])
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


