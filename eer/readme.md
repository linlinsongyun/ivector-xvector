### 0 准备模型
exp/vector_nnet_1a下应该有
extract.config  final.raw  max_chunk_size  min_chunk_size  nnet.config  srand  xvectors_train
其中xvectors_train是文件夹，里边有
mean.vec  plda  transform.mat
### 1. python gen_trials.py wav_dir en_spk.txt or test_spk.txt
data_dir:
会生成txt的文件和trials文件
其中txt包括 wav_path spk
trials 包括 true_spk compared_utt_id target/nontarget
==(utt_id的组成是 spk+'-'+utt_name)==
### 2. sh enroll.sh en_spk.txt 2
生成在data/enroll里边
包括
utt2spk utt_id spk (utt_id的组成是 spk+'-'+utt_name)
spk2utt spk utt_id
mfcc/vad， etc
### 3. sh test.sh test_spk.txt 2
生成在data/test里边
和enroll.sh有相同的操作，只不过会先删除原有的data/test
### mv trials data/test
### 4. bash plda_scoring.sh save_name
生成的eer scores are in 'pwd'/scores.txt

### 或者2/3/4可以浓缩为 python gen_scores_batch.py
需要修改代码中对应的文件
