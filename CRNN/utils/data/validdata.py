import os

# 训练集，验证集，测试集的路径，如果图片都在一起，路径设置成所以图片所在位置
trainDir = 'C:/Users/Bowell/Desktop/DEEPLEARNING/data2(1)/Desktop/crnn-master/data/images/train'
validDir = 'C:/Users/Bowell/Desktop/DEEPLEARNING/data2(1)/Desktop/crnn-master/data/images/val'
testDir = 'C:/Users/Bowell/Desktop/DEEPLEARNING/data2(1)/Desktop/crnn-master/data/images/test'

train_set = set(os.listdir(trainDir))
val_set = set(os.listdir(validDir))
test_set = set(os.listdir(testDir))

num = len(train_set) + len(val_set) + len(test_set)


def valid_data():
    with open('C:/Users/Bowell/Desktop/DEEPLEARNING/data2(1)/Desktop/crnn-master/data/labels/train.txt') as f:
        train_labels = f.readlines()
        train_labels = {label.replace('\n', '').split(' ')[0] for label in train_labels}
        print('训练集标签有对应的图片：', train_labels.issubset(train_set))

    with open('C:/Users/Bowell/Desktop/DEEPLEARNING/data2(1)/Desktop/crnn-master/data/labels//val.txt') as f:
        val_labels = f.readlines()
        val_labels = {label.replace('\n', '').split(' ')[0] for label in val_labels}
        print('验证集标签有对应的图片：', val_labels.issubset(val_set))

    with open('C:/Users/Bowell/Desktop/DEEPLEARNING/data2(1)/Desktop/crnn-master/data/labels/test.txt') as f:
        test_labels = f.readlines()
        test_labels = {label.replace('\n', '').split(' ')[0] for label in test_labels}
        print('测试集标签有对应的图片：', test_labels.issubset(test_set))


if __name__ == '__main__':
    valid_data()
