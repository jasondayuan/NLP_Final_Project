# NLP Final Project

This repository is heavily based on https://github.com/joshuacnf/paradox-learning2reason.

## 1 Generate RP/LP/RP_SMALL/LP_SMALL

Note that although I use 'RP' or 'LP' to refer to the datasets I used to train the models, the actual datasets I used are scaled-down versions of the original RP/LP datasets, as mentioned in section 2 in the report.

Here, the scaled-down version corresponds to RP_SMALL, LP_SMALL.

```
# Generate RP
bash scripts/1_generate_rp.bash

# Generate LP
bash scripts/2_generate_lp.bash

# Generate RP_SMALL
bash scripts/10_generate_rp_small.bash

# Generate LP_SMALL
bash scripts/11_generate_lp_small.py
```

## 2 Train/Evaluate BERT/GPT2/T5 on RP_SMALL/LP_SMALL

For the sake of simplicity, the commands below are for training/evaluating BERT/GPT2/T5 on RP_SMALL. If you want to train on LP_SMALL, simply change all the 'RP_SMALL' in the commands to 'LP_SMALL'.

Note that after training the BERT model, it is needed to make a slight modfication to the ```config.json``` file of the checkpoint directory. There would be a line saying ```"max_position_embeddings": 512```, and you should change it to ```"max_position_embeddings": 1012``` because the position embedding length has been enlongated before training. But for GPT2 and T5, there is no such issue so no modification is needed.

```
# Train BERT on RP_SMALL
bash scripts/5_train_bert.bash \
0 1 9820 \
 OUTPUT/RP_SMALL/BERT/ \
 --num_train_epochs 20.0 \
 --gradient_accumulation_steps 8 --per_gpu_train_batch_size=2 \
 --train_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_train --val_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_val

# Evaluate BERT on RP_SMALL
bash scripts/6_eval_bert.bash 0 \
    --val_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_test \
    --custom_weight OUTPUT/RP_SMALL/BERT/checkpoint-19

# Train GPT2 on RP_SMALL
bash scripts/12_train_gpt2.bash \
 0 1 9820 \
 OUTPUT/RP_SMALL/GPT2/ \
 --num_train_epochs 20.0 \
 --gradient_accumulation_steps 8 --per_gpu_train_batch_size=2 \
 --train_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_train --val_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_val

# Evaluate GPT2 on RP_SMALL
bash scripts/13_eval_gpt2.bash 0 \
    --val_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_test \
    --custom_weight OUTPUT/RP_SMALL/GPT2/checkpoint-19

# Train T5 on RP_SMALL
bash scripts/7_train_t5.bash \
 0 1 9820 \
 OUTPUT/RP_SMALL/T5/ \
 --num_train_epochs 20.0 \
 --gradient_accumulation_steps 8 --per_gpu_train_batch_size=2 \
 --train_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_train --val_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_val

# Evaluate T5 on RP_SMALL
bash scripts/8_eval_t5.bash 0 \
    --val_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_test \
    --custom_weight OUTPUT/RP_SMALL/T5/checkpoint-19
```

## 3 Constructed dataset in section 3.1.2

In section 3.1.2, I constructed a simple dataset to assess the model's ability to reason. Simply run ```python sample/simple_sample.py``` to generate the dataset.

There are some parameters in ```simple_sample.py``` that you can tweak to adjust the reasoning depth, examples per depth and the number of disturbance rules added.

```
MAX_DEPTH = 6 # Max reasoning depth
EXAMPLES_PER_DEPTH = 500 # Examples per depth
DISTURBANCE_NUM = 0 # Number of disturbance rules added
```

## 4 Generate RP_LIM

First, generate the RP dataset according to section 1 of this README file. Then, run ```python gen_rp_lim.py``` to generate RP_LIM under the directory DATA/RP_LIM_30.

Training the BERT base model on RP_LIM is similar to training on RP_SMALL/LP_SMALL:

```
# Training BERT on RP_LIM
bash scripts/5_train_bert.bash \
 0 1 9820 \
 OUTPUT/RP_LIM_30/BERT/ \
 --num_train_epochs 20.0 \
 --gradient_accumulation_steps 8 --per_gpu_train_batch_size=2 \
 --train_file_path DATA/RP_LIM_30/rp_lim_train_30_redist.json --val_file_path DATA/RP_SMALL/prop_examples.balanced_by_backward.max_6.json_val
```

Evaluating the BERT base model trained on RP_LIM on the constructed dataset:

```
bash scripts/6_eval_bert.bash 0 \
    --val_file_path DATA/SIMPLE/simple_dataset.json \
    --custom_weight OUTPUT/RP_LIM_30/BERT/checkpoint-19
```

## 5 Report and presentation

The report is in the file `Final_Project_Report.pdf`, and the presentation slide is in the file `Project.pptx`.