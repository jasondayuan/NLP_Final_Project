import json
import os

def split_by_rule_num(split_rule_num, data, data_dir, split):
    filename_le = f'prop_examples.balanced_by_backward.max_6.json_{split}_le_{split_rule_num}'
    filename_gt = f'prop_examples.balanced_by_backward.max_6.json_{split}_gt_{split_rule_num}'
    data_le = []
    data_gt = []
    for example in data:
        if len(example['rules']) <= split_rule_num:
            data_le.append(example)
        else:
            data_gt.append(example)
    with open(os.path.join(data_dir, filename_le), 'w') as f:
        json.dump(data_le, f)
    with open(os.path.join(data_dir, filename_gt), 'w') as f:
        json.dump(data_gt, f)

def split_by_rule_num_main():
    version = 'LP'
    split = 'full'
    data_dir = f'/scratch/jason/workspace/project/paradox-learning2reason/DATA/{version}'
    filename = f'prop_examples.balanced_by_backward.max_6.json'

    original_file_path = os.path.join(data_dir, filename)
    print('> Loading')
    with open(original_file_path, 'r') as f:
        data = json.load(f)
    print('> Loaded')
    
    split_by_rule_num(20, data, data_dir, split)

def balance_by_depth(data_path, control_num):
    with open(data_path, 'r') as f:
        data = json.load(f)
    data_balanced = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    for example in data:
        if example['depth'] > 6:
            continue
        if len(data_balanced[example['depth']]) <= control_num:
            data_balanced[example['depth']].append(example)
    balanced_examples = []
    for examples in data_balanced.values():
        balanced_examples += examples
    with open(data_path.replace('.json', '.balanced.json'), 'w') as f:
        json.dump(balanced_examples, f)

def separate_by_label():
    path = '/scratch/jason/workspace/project/paradox-learning2reason/DATA/LP_SMALL/prop_examples.balanced_by_backward.max_6.json_test'
    with open(path, 'r') as f:
        data = json.load(f)
    false_data = []
    true_data = []
    for example in data:
        if example['label'] == 0:
            false_data.append(example)
        else:
            true_data.append(example)
    with open(path.replace('.json', '_false.json'), 'w') as f:
        json.dump(false_data, f)
    with open(path.replace('.json', '_true.json'), 'w') as f:
        json.dump(true_data, f)
    print('false', len(false_data))
    print('true', len(true_data))
    
if __name__ == '__main__':
    separate_by_label()
    # split_by_rule_num_main()

    # path = '/scratch/jason/workspace/project/paradox-learning2reason/DATA/LP/prop_examples.balanced_by_backward.max_6.json_full_gt_20'
    # data_balanced = balance_by_depth(path, 500)

    # versions = ['RP']
    # split = 'full'
    # rule_nums = ['_le_20', '_gt_20']
    # for version in versions:
    #     data_dir = f'/scratch/jason/workspace/project/paradox-learning2reason/DATA/{version}'
    #     for rule_num in rule_nums:
    #         filename = f'prop_examples.balanced_by_backward.max_6.json_{split}' + rule_num
    #         original_file_path = os.path.join(data_dir, filename)
    #         with open(original_file_path, 'r') as f:
    #             data = json.load(f)
    #             print(filename, len(data))