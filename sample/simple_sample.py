import json
import random
from tqdm import tqdm

MAX_DEPTH = 6
EXAMPLES_PER_DEPTH = 500
DISTURBANCE_NUM = 0

def read_vocab(vocab_file):
    vocab = []
    with open(vocab_file, 'r') as fin:
        vocab = [line.strip() for line in fin.readlines()]
    print('vocabulary size: ', len(vocab))
    return vocab

def sample_one_example(vocab, depth):

    num_preds = depth + 1
    num_rules = depth
    preds = random.sample(vocab, num_preds)
    example = {}
    example['preds'] = preds
    example['label'] = 1
    example['query'] = preds[-1]
    example['facts'] = [preds[0]]
    rules = []

    for i in range(num_rules):
        rule = []
        rule.append([preds[i]])
        rule.append(preds[i + 1])
        rules.append(rule)

    for i in range(DISTURBANCE_NUM):
        head = preds[0]
        tail = preds[0]
        while head in example['preds'] or tail in example['preds']:
            head = random.choice(vocab)
            tail = random.choice(vocab)
        rule = []
        rule.append([head])
        rule.append(tail)
        rules.append(rule)
        example['preds'].append(head)
        example['preds'].append(tail)

    example['rules'] = rules
    example['depth'] = depth

    return example

def samples_examples(vocab, control_num):
    examples = []
    for _ in range(control_num):
        for depth in range(MAX_DEPTH + 1):
            example = sample_one_example(vocab, depth)
            examples.append(example)
    return examples

if __name__ == "__main__":
    vocab = read_vocab('sample/vocab.txt')
    examples = samples_examples(vocab, EXAMPLES_PER_DEPTH)
    with open('DATA/SIMPLE/simple_dataset.json', 'w') as fout:
        json.dump(examples, fout)
    