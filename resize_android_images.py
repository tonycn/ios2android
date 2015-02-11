#! /usr/bin/env python
# coding=utf-8
import os
from os import listdir
from os.path import isfile, join, isdir
from shutil import copyfile
import sys
from subprocess import call

__author__ = 'matheusjardimb'

# ios2android.py path comes into sys.argv[0]
if len(sys.argv) != 2:
    print('usage: ios2android.py [path | file.zip]')
    exit(-1)

retina_sufix_3x = '@3x'
retina_sufix_2x = '@2x'
retina_sufix_1x = '@1x'

allowed_extensions = ['.png']

res = 'res'
res_ldpi = 'res/drawable-ldpi'
res_mdpi = 'res/drawable-mdpi'
res_hdpi = 'res/drawable-hdpi'
res_xhdpi = 'res/drawable-xhdpi'
res_xxhdpi = 'res/drawable-xxhdpi'
res_dirs = [res, res_ldpi, res_mdpi, res_hdpi, res_xhdpi, res_xxhdpi]


def sanitize_filename(name):
    new_filename = name.replace(retina_sufix_1x, '')
    new_filename = new_filename.replace(retina_sufix_2x, '')
    new_filename = new_filename.replace(retina_sufix_3x, '')
    new_filename = new_filename.replace('-', '_')
    new_filename = new_filename.lower()
    return new_filename


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def move_files_in_dir(path_of_images):
    if path_of_images.endswith('.zip'):
        import zipfile

        unzip_dir = 'unzipped'
        with zipfile.ZipFile(path_of_images, "r") as z:
            z.extractall(unzip_dir)
        path_of_images = unzip_dir

    if not isdir(path_of_images):
        return;

    for filename in listdir(path_of_images):
        fullpath = join(path_of_images, filename)
        new_name = sanitize_filename(filename)

        path = res_xxhdpi
        dst_path = os.path.join(path, new_name)
        src_path = os.path.join(path_of_images, filename)
        copyfile(src_path, dst_path)

        retina_sufix_2x = os.path.join(res_xhdpi, new_name)
        cmd = "convert " +fullpath + " -resize 66.66667%  " + retina_sufix_2x
        os.system(cmd);


        hdpi_dst_path = os.path.join(res_hdpi, new_name)
        cmd = "convert " +fullpath + " -resize 50%  " + hdpi_dst_path
        os.system(cmd);
        pass

if __name__ == '__main__':
    for directory in res_dirs:
        create_dir(directory)
    path = sys.argv[1]
    move_files_in_dir(path)

