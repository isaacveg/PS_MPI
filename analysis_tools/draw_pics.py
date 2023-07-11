import os
from os.path import join as ospj
import yaml
from matplotlib import pyplot


result_root = './results/'

draw_requirements = {
    'meta_method': ['fedavg', 'fomaml', 'mamlhf']
    ,'inner_lr': [0.1, 0.01]
    ,'outer_lr': [0.01, 0.05]
    ,'num_epochs': [200]
}

draw_contents = [
    'acc_bf_adpt'
    ,'acc_af_adpt'
    ,'loss_bf_adpt'
    ,'loss_af_adpt'
    ,'test_acc'
    ,'test_loss'
    # ,''
]


def main():
    # 获取文件夹下的所有一级子文件夹名称
    subfolders = [ospj(result_root, f) for f in os.listdir(result_root)]
    # print(subfolders)
    # 获取每次结果对应的config文件信息
    cfgs = [get_config(f) for f in subfolders]
    # 获取每次结果对应的server_log文件目录
    server_logs = [ospj(subfolder, os.path.basename(subfolder) + "_server.log") for subfolder in subfolders]
    # print(server_logs)

    # 获取符合 draw_requirements 的 config 以及对应的信息
    acquired_cfgs = []
    # 遍历 config
    for idx, cfg in enumerate(cfgs):
        for key, value in draw_requirements.items():
            # 如果有一个不满足要求则跳过，否则加入列表
            if cfg[key] not in value:
                continue
        acquired_cfgs.append((idx, cfg))
    
    # 将draw_contents里的内容画到一张图里

    ## 画准确率部分
    fig = pyplot.figure()
    # 读取server_log中的acc_bf_adpt信息并画图
    if 'acc_bf_adpt' in draw_contents:
        pic = pyplot.figure()
        acc_bf = []
        acc_af = []
        for idx, cfg in acquired_cfgs:
            # 打开文件，获取信息
            pass

    
    if 'acc_af_adpt' in draw_contents:
        pass

    if 'test_acc' in draw_contents:
        pass

    ## 画损失部分
    # 读取server_log中的loss_bf_adpt信息并画图
    if 'loss_bf_adpt' in draw_contents:
        pic = pyplot.figure()
        loss_bf = []
        acc_bf = []
        for idx, cfg in acquired_cfgs:
            # 打开文件，获取信息
            pass

    
    if 'loss_af_adpt' in draw_contents:
        pass

    if 'test_loss' in draw_contents:
        pass      
                

    

def process_server_log(filename, cfg):
    with open(filename, 'r') as f:
        lines = f.readlines()   
        train_data, eval_data, global_data = [],[],[]
        epoch_cnt = 0
        eval_round = cfg['eval_round']
        eval_training = cfg['eval_while_training']
        for line in lines:
            if 'Epoch:' in line:
                epoch_cnt += 1
            elif 'Selected client idxes' in line and eval_training:
                if epoch_cnt % eval_round == 0:
                    train_data.append({})
                    eval_acc_before = float(lines[lines.index(line)+1].split(': ')[1])
                    eval_acc_after = float(lines[lines.index(line)+2].split(': ')[1])
                    eval_loss_before = float(lines[lines.index(line)+3].split(': ')[1])
                    eval_loss_after = float(lines[lines.index(line)+4].split(': ')[1])
                    train_data[-1]['eval_acc_before'] = eval_acc_before
                    train_data[-1]['eval_acc_after'] = eval_acc_after
                    train_data[-1]['eval_loss_before'] = eval_loss_before
                    train_data[-1]['eval_loss_after'] = eval_loss_after
            elif 'Evaling clients' in line:
                if epoch_cnt % eval_round == 0:
                    train_data.append({})
                    eval_acc_before = float(lines[lines.index(line)+1].split(': ')[1])
                    eval_acc_after = float(lines[lines.index(line)+2].split(': ')[1])
                    eval_loss_before = float(lines[lines.index(line)+3].split(': ')[1])
                    eval_loss_after = float(lines[lines.index(line)+4].split(': ')[1])
                    eval_data[-1]['eval_acc_before'] = eval_acc_before
                    eval_data[-1]['eval_acc_after'] = eval_acc_after
                    eval_data[-1]['eval_loss_before'] = eval_loss_before
                    eval_data[-1]['eval_loss_after'] = eval_loss_after
            elif 'Test_Loss' in line:
                test_loss = float(line.split(': ')[1])
                test_acc = float(lines[lines.index(line)+1].split(': ')[1])
                global_data[-1]['test_loss'] = test_loss
                global_data[-1]['test_acc'] = test_acc
    return train_data, eval_data, global_data

# 
def get_config(path_name):
    filename = ospj(path_name,'config.yml')
    with open(filename, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    return cfg



if __name__ == "__main__":
    main()
