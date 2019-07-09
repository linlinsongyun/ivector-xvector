#export KALDI_ROOT=/home/zhangying09/.jupyter/kaldi-master
export KALDI_ROOT=/opt/kaldi
[ -f $KALDI_ROOT/tools/env.sh ] && . $KALDI_ROOT/tools/env.sh

export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/tools/sph2pipe_v2.5:$PWD:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh
export LC_ALL=C

export LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda-9.0/lib64:$LD_LIBRARY_PATH
# there is no utils in the dictionary, then add link to original kaldi
ln -s $KALDI_ROOT/egs/sre16/v2/steps ./
ln -s $KALDI_ROOT/egs/sre16/v2/sid ./
ln -s $KALDI_ROOT/egs/sre16/v2/utils ./
