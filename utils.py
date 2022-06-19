import os
import json
import pickle
import random
import codecs
import sys
import gzip
import math
import opencc

import time


def timestamp2time(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, " is created")
    else:
        print(path, " already exists")


def json_write(data, filename):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        print("成功保存文件{}".format(str(filename)))


def json_read(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        return json.load(f)


def pkl_read(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def pkl_write(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def txt_read(filename):
    out_list = []
    with open(filename, 'r', encoding="utf-8", ) as f:
        for line in f:
            if line is not None:
                out_list.append(line.strip())
    return out_list


# 保存
def txt_save(input_list, filename):
    with open(filename, 'w', encoding="utf-8", ) as f:
        for i in input_list:
            f.write(str(i) + '\n')


def read_text8(filename):
    """
    read your own data.
    :param filename:
    :return:
    """
    print('reading data...')
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read().split()
    print('corpus size', len(data))
    return data


# 将list转成字符串，中间用空格隔开
def list2str(input_list):
    return " ".join(str(i) for i in input_list)


def traditional2simplified(input_string):
    converter = opencc.OpenCC('t2s.json')
    out = converter.convert(input_string)  # 漢字
    return out


# data为2维，每一列代表一个特征，注意广播机制
def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma



# ["aaa fdf","ffdsdf"] → ["aaa", "fdf","ffdsdf"]
def concat_sentence(input):
    out = []
    for sentence in input:
        out.extend(sentence.strip().split())
    return out


# 列表返回索引
def list2index(input:list):
    out = [i for i,v in enumerate(input)]
    return out



def unzip(input):
    x, y, z = [], [], []
    for item in input:
        x.append(item[0])
        y.append(item[1])
        z.append(item[2])
    return x, y, z

# 打乱batch
# input:x,y,z = [1,2,3],[[4,5,6],[5,3,6],[3,3,3]],[[7,8,9],[8,7,9],[8,8,8]]
# x_,y_,z_ = shuffle_batch(x,y,z)
# return:x_,y_,z_ = [3, 2, 1] [[3, 3, 3], [5, 3, 6], [4, 5, 6]] [[8, 8, 8], [8, 7, 9], [7, 8, 9]]
def shuffle_batch(x,y,z):
    shuffle_batch = [list(item) for item in zip(x, y, z)]
    random.shuffle(shuffle_batch)
    x_, y_, z_ = unzip(shuffle_batch)
    return x_,y_,z_

# 返回文件夹下所有文件的路径
def get_files_list(raw_dir):
    files_list = []
    for filepath,dirnames,filenames in os.walk(raw_dir):
        for filename in filenames:
            files_list.append(filepath+'/'+filename)
    return files_list



if __name__ == '__main__':
    pass
