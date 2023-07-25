import os, fnmatch
from os.path import join as ospj
import yaml
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('Agg')
matplotlib.rcParams['savefig.format'] = 'png'

result_root = './results/'
plot_root = './plot/'

if not os.path.exists(plot_root):
    os.makedirs(plot_root)
if not os.path.exists(result_root):
    os.makedirs(result_root)

draw_requirements = {
    'epoch_num': [5]
    # ,'data_partition_pattern':[1]
    # ,'non_iid_ratio': [7]
}

draw_contents = [
    'train_acc'
    ,'train_loss'
    ,'eval_acc'
    ,'eval_loss'
    ,'test_acc'
    ,'test_loss'
]


def main():
    # 获取文件夹下的所有一级子文件夹名称
    subfolders = [ospj(result_root, f) for f in os.listdir(result_root)]
    # print(subfolders)
    # 获取每次结果对应的config文件信息
    cfgs = [get_config(f) for f in subfolders]
    # 获取每次结果对应的server_log文件目录
    server_logs = [ospj(subfolder, filename) for subfolder in subfolders for filename in os.listdir(subfolder) if fnmatch.fnmatch(filename, '*server.log')]    
    print(server_logs)

    # 获取符合 draw_requirements 的 config 以及对应的信息
    acquired_cfgs = []
    # 遍历 config
    for idx, cfg in enumerate(cfgs):
        flag = 0
        for key, value in draw_requirements.items():
            # 如果有一个不满足要求则跳过，否则加入列表
            if cfg[key] not in value:
                flag = 1
                break
        if flag == 0:acquired_cfgs.append((idx, cfg))
    
    print([cfg[0] for cfg in acquired_cfgs])

    ## 画准确率部分
    plt.figure()
    for idx, cfg in acquired_cfgs:
        if 'train_acc' in draw_contents:
            loss, acc = process_server_log(server_logs[idx])
            epochs = [i for i in range(len(acc))]

            result_str = "_".join([ str(cfg[item]) for item in draw_requirements.keys()])

            plt.plot(epochs, acc, label='acc_'+result_str)


    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Global Model Accuracy')
    plt.legend() 
    plt.savefig(plot_root+'/train_acc.png')

    plt.figure()
    for idx, cfg in acquired_cfgs:
        if 'train_acc' in draw_contents:
            loss, acc = process_server_log(server_logs[idx])
            epochs = [i for i in range(len(acc))]

            result_str = "_".join([ str(cfg[item]) for item in draw_requirements.keys()])

            plt.plot(epochs, loss, label='acc_'+result_str)

    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Global Model Loss')
    plt.legend() 
    plt.savefig(plot_root+'/train_loss.png')
        
    


def process_server_log(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()   
        t_loss, t_acc = [], []
        epoch_cnt = 0
        line_cnt = 0
        for line in lines:
            if 'Epoch:' in line:
                epoch_cnt = int(line.split(': ')[1])
            elif 'Test_Loss' in line:
                t_loss.append(float(line.split(': ')[1]))
            elif 'Test_Acc' in line:
                t_acc.append(float(line.split(': ')[1]))
            line_cnt += 1
    return t_loss, t_acc

# 
def get_config(path_name):
    filename = ospj(path_name,'config.yml')
    with open(filename, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    return cfg



if __name__ == "__main__":
    main()
