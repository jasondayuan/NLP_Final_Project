import os
import json

if __name__ == '__main__':
    version = 'RP_SMALL'
    splits = ['train', 'val', 'test']
    for split in splits:
        data_path = f'./DATA/{version}/prop_examples.balanced_by_backward.max_6.json_{split}'
        with open(data_path, 'r') as f:
            data = json.load(f)
            print(f'{split}: {len(data)}')