import os
import json
import random

if __name__ == '__main__':
    max_rule_num = 30
    save_dir = f'./DATA/RP_LIM_{max_rule_num}'
    rp_file_path = './DATA/RP/prop_examples.balanced_by_backward.max_6.json'
    random.seed(0)
    with open(rp_file_path, 'r') as f:
        data = json.load(f)
    random.shuffle(data)

    depths = [0, 1, 2, 3, 4, 5, 6]
    lim_data_true = {}
    lim_data_false = {}
    for depth in depths:
        lim_data_true[depth] = []
        lim_data_false[depth] = []
    
    # Categorize data
    for example in data:
        if len(example['rules']) <= max_rule_num:
            if example['label'] == 1:
                lim_data_true[example['depth']].append(example)
            else:
                lim_data_false[example['depth']].append(example)

    # Redistribute data
    # 1. Examples with depth 0/1 should be no more than 3200 in the training set
    # 2. Other examples are sampled freely
    examples_per_depth = [3200, 3200, 4800, 4600, 3200, 2400, 1000]
    data_lim = []
    for depth in depths:
        data_lim += lim_data_true[depth][:examples_per_depth[depth] // 2]
        data_lim += lim_data_false[depth][:examples_per_depth[depth] // 2]
    random.shuffle(data_lim)
    
    # Show statistics of data_lim
    for depth in depths:
        true_num = len([example for example in data_lim if example['depth'] == depth and example['label'] == 1])
        false_num = len([example for example in data_lim if example['depth'] == depth and example['label'] == 0])
        print(f'Depth: {depth} Total: {true_num + false_num} True percentage: {true_num / (true_num + false_num)}')

    with open(os.path.join(save_dir, f'rp_lim_train_{max_rule_num}_redist.json'), 'w') as f:
        json.dump(data_lim, f, indent=4)
