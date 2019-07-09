. ./cmd.sh
. ./path.sh
set -e

datadir=`pwd`/data
logdir=`pwd`/data/log
enroll_featdir=`pwd`/data/enroll/feat
test_featdir=`pwd`/data/test/feat
nnet_dir=`pwd`/exp/xvector_nnet_1a
test_trials=`pwd`/data/test/trials
mean_dir=`pwd`/data/feat/xvectors_enroll_mfcc

if [ $# != 1 ] ; then
        echo "USAGE: $0 target model(or speaker_path) type"
        exit 1;
fi

score_name=$1

stage=1
#<<'COMMENT'
if [ $stage -le 11 ]; then
  # Compute PLDA scores for SITW dev core-core trials
  $train_cmd $logdir/jn_vector_scoring.log \
    ivector-plda-scoring --normalize-length=true \
      "ivector-copy-plda --smoothing=0.0 $nnet_dir/xvectors_train/plda - |" \
      "ark:ivector-mean ark:data/enroll/spk2utt scp:$enroll_featdir/xvectors_enroll_mfcc/xvector.scp ark:- | ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec ark:- ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
      "ark:ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec scp:$test_featdir/xvectors_test_mfcc/xvector.scp ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
      "cat '$test_trials' | cut -d\  --fields=1,2 |" $datadir/test_scores || exit 1;
    echo ==========================================
    echo ivector-plda-scoring end
    echo  ==========================================
fi
if [ $stage -le 12 ]; then
  echo 'begin comput eer'
  # SITW Dev Core:
  # EER: 3.003%
  # minDCF(p-target=0.01): 0.3119
  # minDCF(p-target=0.001): 0.4955
  eer=$(paste $test_trials $datadir/test_scores | awk '{print $6, $3}' | compute-eer - 2>/dev/null)
  mindcf1=`sid/compute_min_dcf.py --p-target 0.01 $datadir/test_scores $test_trials  2> /dev/null`
  mindcf2=`sid/compute_min_dcf.py --p-target 0.001 $datadir/test_scores $test_trials  2> /dev/null`

  echo "$score_name" >>scores.txt
  echo "EER: $eer% ">> scores.txt
  echo "minDCF(p-target=0.01): $mindcf1 ">> scores.txt
  echo "minDCF(p-target=0.001): $mindcf2 ">>scores.txt

fi
