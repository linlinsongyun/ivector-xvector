# 1. 下载训练好的模型
for 16k wav model, u should use kaldi/egs/voxceleb/ \
v1 for ivector\
v2 for xvector 其中exp中的文件单独挪出来，放在xvector的目录下，方便直接调用
download the model from http://www.kaldi-asr.org/models/m7

替换原目录下的exp/local等文件夹

## 2. 单独准备过程（已省略）
1. 提取wav的txt文件  其中wav_dir = name/wav/**.wav
```
python generate_speaker.py wav_dir save_txt
```
2.提取wav.scp utt2spk(注意当前目录下不能有同名文件，否则是接着写而不是覆盖）
`python 01.py wav_dir`

3. 顺序排列在data文件夹下（enroll.sh默认读取的路径，初始不存在）
```
sort wav.scp >>data/wav.scp
sort utt2spk >>data/utt2spk
perl kaldi/egs/timit/s5/utils/utt2spk_to_spk2utt.pl utt2spk > spk2utt
```

### 3. x-vector 提取过程
1. 修改path.sh的kaldi路径,  软连接ln ** 打开
2. 检查conf对应的文件是否是16khz，可以copy kaldi voxcelb的
3. cp steps utils的文件夹到当前目录
3. 提取x-vector
（1）生成wav的txt文件  其中wav_dir = name/wav/**.wav
```
python generate_speaker.py wav_dir save_txt
```
wav_dir SPK WAV_NAME


（2）注意看 make_data_speaker.py的文件读是否正确
case1: 不区分说话人
`bash enroll.sh speaker.txt 1`

case2: 区分说话人
`bash enroll.sh speaker.txt 2`

4. 单句的xvector变成单人的xvector

```
transform-vec exp/xvector_nnet_1a/xvectors_train/transform.mat ark:data/feat/xvectors_enroll_mfcc/spk_xvector.ark ark:- | ivector-normalize-length ark:- ark:vctk10-spk-xvec.ark
```
2. ark文件转成txt文件
```
 copy-vector ark:xvec-spk-tranfrom-nor.ark ark,t:- >xvec-spk-tranfrom-nor.txt
```
 3. 转成模型训练可用的vector-npy
 ```
python ../vec2npy.py vecror.txt save_dir
 ```

###### 4. 分解步骤


 - dir ---`exp/xvector_nnet_1a/xvectors_train/transform.mat`
 - lda分析降维
 `transform-vec exp/xvector_nnet_1a/xvectors_train/transform.mat ark:data/feat/xvectors_enroll_mfcc/spk_xvector.ark ark:xvec-spk-tranfrom.ark`
 - 做norm-length
```
 ivector-normalize-length ark:xvec-spk-tranfrom.ark ark:xvec-spk-tranfrom-nor.ark
```

` ivector-normalize-length`在`kaldi/src/ivectorbin`路径下



### debug

1.维度不匹配

```
ERROR (nnet3-xvector-compute[5.4.198~1-be7c1]:AcceptInput():nnet-compute.cc:556) Num-cols mismatch for input 'input': 30 in computation-request, 23 provided.
```
在提x-vector的步骤报错，检查conf文件的是否正确，需要的是16khz的配置

2.报错 parse_option找不到

```
. parse_options.sh || exit 1;
```
path路径的软连接释放， 在utils/parse_option.sh

3. 
`nnet3-xvector-compute: error while loading shared libraries: libcudart.so.9.0: cannot open shared object file: No such file or directory`

把对应的cuda lib路径加在bashrc中，source ～/.bashrc更新一下
```
export PATH=$PATH:/usr/local/cuda-8.0/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-8.0/lib64
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/cuda-8.0/lib64
```


## Files List

 `ivector/`
  - `conf/`: configure file for mfcc and vad
  - `wav/`: test audio  (you can also use your own wav path, see **Step 1**)
    - Only supprot flac (install flac), wav and sph (install sph2pipe )
  - `model_3000h/`: pre-trained model
  - `enroll.sh`: main process fille


  - `data/`: save extracted features (It's a generated file)
    - `utt2spk, wav.scp` generate two files through make_data.py
    - `spk2utt`: generate from utt2spk
    - `log/`: save all logs
    - `tmp/`: save all tmp files


`xvector/`

- `conf/`: configure file for mfcc and vad
- `wav/`: test audio  (you can also use your own wav path, see **Step 1**)
  - Only supprot flac (install flac), wav and sph (install sph2pipe )
- `exp/`: pre-trained model
- `enroll.sh`: main process fille


- `data/`: save extracted features (It's a generated file)
  - `utt2spk, wav.scp` generate two files through make_data.py
  - `spk2utt`: generate from utt2spk
  - `log/`: save all logs
  - `tmp/`: save all tmp files

`format_norm.py`: change ark format to npz format

## Extract features: ivector and xvector

### Step 0: Preparation

- First, install [Kaldi](https://github.com/kaldi-asr/kaldi). 
- Then, step into `ivector/` or `xvector/` folder


- Change KALDI_ROOT in `path.sh` to your own kaldi root
- Add link:

```sh
ln -s $KALDI_ROOT/egs/sre16/v2/steps ./
ln -s $KALDI_ROOT/egs/sre16/v2/sid ./
ln -s $KALDI_ROOT/egs/sre16/v2/utils ./
```



### Step 2: Read generate ivector and xvector

In this section, we convert ivector and xvector from ark type to array type

i-vector in `data/feat/ivectors_enroll_mfcc`

- `spk_ivector.ark` i-vector for each speaker
- `ivector.1.ark`: i-vector for each utturance (400-d i-vector)

x-vector in `data/feat/xvectors_enroll_mfcc`

- `spk_xvector.ark` x-vector for each speaker
- `xvector.1.ark`: x-vector for each utturance (512-d x-vector)

```sh
## print name and feats from ark to txt
$KALDI_ROOT/src/bin/copy-vector ark:ivector/data/feat/ivectors_enroll_mfcc/ivector.1.ark ark,t:- >ivector.txt

$KALDI_ROOT/src/bin/copy-vector ark:xvector/data/feat/xvectors_enroll_mfcc/xvector.1.ark ark,t:- >xvector.txt

## Or you can change ark format to np.array format, which has (data_path ['pic_path'], ivector or xvector)
python format_norm.py --vector_path='xvector.txt' --save_path='x_vector.npz'
python format_norm.py --vector_path='ivector.txt' --save_path='i_vector.npz'
```

# Other summary

```sh
## combine different files
utils/combine_data.sh

## make xxx fits to the kaldi format
utils/fix_data_dir.sh xxx

## gain subset of data
utils/subset_data_dir.sh

## file exists and dir exists
if [ -d "./data" ];then # dictionary exists
if [ -f "./data/1.txt" ];then # file exists

## xvector/run.sh
Has four folder: 
	sre_combined (source domain, argument data, for training)
	sre16_major (unlabeded target domain for model adaption)
	sre16_eval_enroll(labeded target domain for train)
	sre16_eval_test(unlabeded target domain for test)
Main stream: xvector->mean->transform(LDA)->len normalize->classifier(PLDA/adapt-PLDA)

## ark: split by space and print the third one
echo '1 2 3' |awk '{print $3}'  # print 3
```

# python vec2txt.py xx.txt save_dir
讲txt中各个的vector单独写出来，保存成一个文件

