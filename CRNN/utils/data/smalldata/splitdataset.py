import os
from shutil import copy2
import tqdm
from joblib import Parallel, delayed
import random

# 所有图片所在位置（自己改）
image_dir = "C:/Users/Bowell/Desktop/DEEPLEARNING/data2(1)/Desktop/data2/cropped_image/"
all_data = os.listdir(image_dir)
random.seed(9)
random.shuffle(all_data)
num_all_data = len(all_data)

trainDir = "../../../data/images/train"  # （将训练集放在这个文件夹下）
if not os.path.exists(trainDir):
    os.mkdir(trainDir)
validDir = '../../../data/images/val'  # （将验证集放在这个文件夹下）
if not os.path.exists(validDir):
    os.mkdir(validDir)
testDir = '../../../data/images/test'  # （将测试集放在这个文件夹下）
if not os.path.exists(testDir):
    os.mkdir(testDir)

ftrain = open('../../../data/labels/train.txt', 'w+', encoding='gbk')
fval = open('../../../data/labels/val.txt', 'w+', encoding='gbk')
ftest = open('../../../data/labels/test.txt', 'w+', encoding='gbk')


def split_labels():
    with open('../../../data/labels.txt', encoding='gbk') as f:
        labels = f.readlines()
    print(labels)
    train_data = os.listdir(trainDir)
    val_data = os.listdir(validDir)
    test_data = os.listdir(testDir)
    print(train_data)
    i = 0
    for label in labels:
        img_name = label.split(' ')[1]+' '+label.split(' ')[2]
        img_names = label.split(' ')[1]
        print(img_name)
        if img_names in train_data:
            ftrain.write(img_name)
        elif img_names in val_data:
            fval.write(img_name)
        elif img_names in test_data:
            ftest.write(img_name)
        i += 1


def split_images(i):
    if i < num_all_data * 0.75:
        copy2(image_dir + all_data[i], trainDir)
    elif i < num_all_data * 0.95:
        copy2(image_dir + all_data[i], validDir)
    else:
        copy2(image_dir + all_data[i], testDir)


if __name__ == '__main__':
    Parallel(n_jobs=8)(delayed(split_images)(i) for i in tqdm.tqdm(range(0, num_all_data)))
    split_labels()
