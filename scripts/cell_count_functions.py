#Run cell counting
import os
import skimage
from skimage import io
from skimage.transform import resize
import torch
from IPython.display import Image, clear_output  # to display images
import subprocess
import glob

def run_count(orig_dir):


    pics = os.listdir(orig_dir)

    for pic in pics:
        resize_256(orig_dir, pic)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    resized_path = os.path.join(script_dir, "workspace", "1_resized")
    #print(resized_path)
    os.chdir(os.path.join(script_dir, "yolov5-master"))
    os.system('python detect.py --weights "../weights/256_box/last_591.pt" --img 256 --conf 0.25 --source "' + resized_path + '" --save-txt --name last_run_crop')

    os.system("rm ../workspace/1_resized/*")

    crop_label_files = os.listdir(os.path.join(get_latest_file(os.path.join(script_dir,'yolov5-master/runs/detect'), 'last_run_crop*'), 'labels'))
    for label_file in crop_label_files:
        crop_4by4(orig_dir,label_file)


    cropped_path = os.path.join(script_dir, "workspace", "2_cropped")
    os.system('python detect.py --weights "../weights/cropped_cells/best_203.pt" --img 1024 --conf 0.375 --source "' + cropped_path + '" --save-txt --name last_run_cells --line-thickness 1')
    #output = subprocess.check_output(['python', 'detect.py', '--weights','"../weights/cropped_cells/best_203.pt"','--img' ])
    os.system('rm ../workspace/2_cropped/*')
    return



def resize_256(orig_dir,pic):
    img = io.imread(os.path.join(orig_dir,pic))
    img_256 = resize(img, (256,256))
    resized_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace", "1_resized")
    io.imsave(resized_path + '/' + pic, img_256)
    return

def get_latest_file(path, *paths):
    """Returns the name of the latest (most recent) file
    of the joined path(s)"""
    fullpath = os.path.join(path, *paths)
    list_of_files = glob.glob(fullpath)  # You may use iglob in Python3
    if not list_of_files:                # I prefer using the negation
        return None                      # because it behaves like a shortcut
    latest_file = max(list_of_files, key=os.path.getctime)
    _, filename = os.path.split(latest_file)
    return os.path.join(path,filename)

def crop_4by4(orig_dir,label_file):
    crop_label = open(os.path.join(get_latest_file('runs\\detect', 'last_run_crop*'),'labels', label_file), 'r')
    coord = crop_label.readline().rstrip().split()
    cx_center, cy_center, cwidth, cheight = float(coord[1]), float(coord[2]), float(coord[3]), float(coord[4])
    img = io.imread(os.path.join(orig_dir,label_file[:-3] + 'jpg'))
    crop_x_start = int((cx_center - 0.5*cwidth*1.15)*img.shape[1])
    crop_x_end = int((cx_center + 0.5*cwidth*1.15)*img.shape[1])
    crop_y_start = int((cy_center - 0.5*cheight*1.15)*img.shape[0])
    crop_y_end = int((cy_center + 0.5*cheight*1.15)*img.shape[0])
    cropped = img[crop_y_start:crop_y_end, crop_x_start:crop_x_end]
    cropped_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace", "2_cropped")
    io.imsave(cropped_path + '/' + label_file[:-3] + 'jpg', cropped)
