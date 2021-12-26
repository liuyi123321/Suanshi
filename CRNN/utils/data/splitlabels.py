import tqdm

ftrain = open('C:/Users/fly tree/Desktop/crnn-master/data/labels/train.txt', 'w+')
fval = open('C:/Users/fly tree/Desktop/crnn-master/data/labels/val.txt', 'w+')
ftest = open('C:/Users/fly tree/Desktop/crnn-master/data/labels/test.txt', 'w+')


def split_labels():
    with open('C:/Users/fly tree/Desktop/data2/txt/image2label.txt') as f:
        labels = f.readlines()
        for i in range(len(labels)):
            start = labels[i].index('_') - 1
            labels[i] = labels[i][start:]
    num = len(labels)

    i = 0
    for label in tqdm.tqdm(labels):
        if i < num * 0.75:
            ftrain.write(label)
        elif i < num * 0.95:
            fval.write(label)
        else:
            ftest.write(label)
        i += 1


if __name__ == '__main__':
    split_labels()
