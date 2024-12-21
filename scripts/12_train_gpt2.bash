mkdir -p $4

CUDA_VISIBLE_DEVICES=$1 python -m torch.distributed.launch --master_port=$3 --nproc_per_node=$2 finetune_simplified_gpt2.py \
    --model_type gpt2 \
    --tokenizer_name=gpt2 \
    --model_name_or_path gpt2 \
    --config_name gpt2 \
    --do_train \
    --do_eval \
    --do_lower_case \
    --save_steps -1 \
    --per_gpu_eval_batch_size=1 \
    --per_gpu_train_batch_size=1 \
    --learning_rate 4e-5 \
    --overwrite_output_dir \
    --logging_steps 50 \
    --num_workers 1 \
    --warmup_steps 0.05 \
    --max_length 1024 \
    --seed 10 \
    --output_dir $4 \
    ${@:5}

