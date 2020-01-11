### 1. python gen_trials.py data_dir en_spk.txt or test_spk.txt
data_dir:
会生成txt的文件和trials文件
### 2. sh enroll.sh en_spk.txt 2
生成在data/enroll里边
### 3. sh test.sh test_spk.txt 2
生成在data/test里边
### mv trials data/test
### 4. bash plda_scoring.sh save_name
eer scores are in 'pwd'/scores.txt

### 或者2/3/4可以浓缩为 python gen_scores_batch.py
需要修改代码中对应的文件
