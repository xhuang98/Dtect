import os
import random
from tqdm import tqdm
from shutil import copyfile


if __name__ == '__main__':
    random.seed(10)

    data_dir = "D:\\los alamos\\auths"
    files = [filename for filename in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, filename))]

    train_size = int(len(files) * 0.7)
    validation_size = int(len(files) * 0.2)
    test_size = len(files) - train_size - validation_size
    print(f"{len(files)} files in total. {train_size} train, {validation_size} validation, {test_size} test.")

    random.shuffle(files)
    train = files[:train_size]
    validation = files[train_size: train_size + validation_size]
    test = files[train_size + validation_size:]

    print("training set")
    os.mkdir(os.path.join(data_dir, "train"))
    for filename in tqdm(train):
        copyfile(os.path.join(data_dir, filename), os.path.join(data_dir, "train", filename))
    print("validation set")
    os.mkdir(os.path.join(data_dir, "validation"))
    for filename in tqdm(validation):
        copyfile(os.path.join(data_dir, filename), os.path.join(data_dir, "validation", filename))
    print("test set")
    os.mkdir(os.path.join(data_dir, "test"))
    for filename in tqdm(test):
        copyfile(os.path.join(data_dir, filename), os.path.join(data_dir, "test", filename))
