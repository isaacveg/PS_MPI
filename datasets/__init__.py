import random
import numpy as np
from torch.utils.data import DataLoader
# from torchvision import datasets as ds

# import datasets
# from datasets import *
import datasets.CIFAR10
import datasets.CIFAR100
import datasets.FashionMNIST
import datasets.MNIST
import datasets.SVHN
import datasets.EMNIST
import datasets.tinyImageNet
import datasets.image100
# add your own datasets 


from config import cfg

class Partition(object):
    """
    按要求划分数据集
    """
    def __init__(self, data, index):
        self.data = data
        self.index = index

    def __len__(self):
        return len(self.index)

    def __getitem__(self, index):
        data_idx = self.index[index]
        return self.data[data_idx]
    

class RandomPartitioner(object):
    """
    随机划分数据集
    """
    def __init__(self, data, partition_sizes, seed=2023):
        self.data = data
        self.partitions = []
        rng = random.Random()
        rng.seed(seed)

        data_len = len(data)
        indexes = [x for x in range(0, data_len)]
        rng.shuffle(indexes)

        for frac in partition_sizes:
            part_len = round(frac * data_len)
            self.partitions.append(indexes[0:part_len])
            indexes = indexes[part_len:]

    def use(self, partition):
        selected_idxs = self.partitions[partition]

        return selected_idxs
    
    def __len__(self):
        return len(self.data)


class LabelwisePartitioner(object):
    """
    根据数据类别划分
    """
    def __init__(self, data, partition_sizes, seed=2024):
        # sizes is a class_num * vm_num matrix
        self.data = data
        self.partitions = [list() for _ in range(len(partition_sizes[0]))]
        rng = random.Random()
        rng.seed(seed)

        label_indexes = list()
        class_len = list()
        # label_indexes includes class_num lists. Each list is the set of indexs of a specific class
        # for class_idx in range(len(data.classes)):
        for class_idx in range(cfg['classes_size']):
            label_indexes.append(list(np.where(np.array(data.targets) == class_idx)[0]))
            class_len.append(len(label_indexes[class_idx]))
            rng.shuffle(label_indexes[class_idx])

        # distribute class indexes to each vm according to sizes matrix
        for class_idx in range(cfg['classes_size']):
            begin_idx = 0
            for vm_idx, frac in enumerate(partition_sizes[class_idx]):
                end_idx = begin_idx + round(frac * class_len[class_idx])
                end_idx = int(end_idx)
                self.partitions[vm_idx].extend(label_indexes[class_idx][begin_idx:end_idx])
                begin_idx = end_idx

    def use(self, partition):
        selected_idxs = self.partitions[partition]
        return selected_idxs
    
    def __len__(self):
        return len(self.data)


def create_dataloaders(dataset, batch_size, selected_idxs=None, shuffle=True, pin_memory=True, num_workers=0):
    if selected_idxs == None:
        dataloader = DataLoader(dataset, batch_size=batch_size,
                                    shuffle=shuffle, pin_memory=pin_memory, num_workers=num_workers)
    else:
        partition = Partition(dataset, selected_idxs)
        dataloader = DataLoader(partition, batch_size=batch_size,
                                    shuffle=shuffle, pin_memory=pin_memory, num_workers=num_workers)
    
    return dataloader


def load_datasets(dataset_type, data_path="/data/docker/data"):
    """
    load datasets and ready for use or partition
    """
    dataset_class = getattr(datasets, dataset_type)
    train_dataset, test_dataset = dataset_class.create_dataset(data_path)

    # if dataset_type == 'CIFAR10':
    #     train_dataset, test_dataset = datasets.CIFAR10.create_dataset(data_path)

    # elif dataset_type == 'CIFAR100':
    #     train_dataset, test_dataset = datasets.CIFAR100.create_dataset(data_path)

    # elif dataset_type == 'FashionMNIST':
    #     train_dataset, test_dataset = datasets.FashionMNIST.create_dataset(data_path)

    # elif dataset_type == 'MNIST':
    #     train_dataset, test_dataset = datasets.MNIST.create_dataset(data_path)
    
    # elif dataset_type == 'SVHN':
    #     train_dataset, test_dataset = datasets.SVHN.create_dataset(data_path)

    # elif dataset_type == 'EMNIST':
    #     train_dataset, test_dataset = datasets.EMNIST.create_dataset(data_path)

    # elif dataset_type == 'tinyImageNet':
    #     train_dataset, test_dataset = datasets.tinyImageNet.create_dataset(data_path)

    # elif dataset_type == 'image100':
    #     train_dataset, test_dataset = datasets.image100.create_dataset(data_path)

    return train_dataset, test_dataset
