#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash

# Copyright 2015   David Snyder
#           2015   Johns Hopkins University (Author: Daniel Garcia-Romero)
#           2015   Johns Hopkins University (Author: Daniel Povey)
# Apache 2.0.
#
# See README.txt for more info on data required.
# Results (EERs) are inline in comments below.
#
# This example script shows how to replace the GMM-UBM
# with a DNN trained for ASR. It also demonstrates the
# using the DNN to create a supervised-GMM.
. ./cmd.sh
. ./path.sh
set -e

if [ $# != 2 ] ; then
        echo "USAGE: $0 wav_path(or speaker_path) type"
        exit 1;
fi

if [[ "$2" = "1" ]] ; then
        wavdir=$1
        DataPre=1
        echo "1: without speaker"
elif [[ "$2" = "2" ]] ; then
        speakerPath=$1
        DataPre=2
        echo "2: with speaker"
else
        echo "Error: type should set to be 1 or 2"
        exit 1;
fi
if [ -d "./data/test" ];then
        rm -rf ./data/test
        rm -rf ./data/test_scores
fi
#COMMENT

FIXDATA=1
FeatureForMfcc=1
VAD=1
EXTRACT=1
DOLDA=1
plda=1
datadir=`pwd`/data/test
logdir=`pwd`/data/test/log
featdir=`pwd`/data/test/feat
nnet_dir=`pwd`/exp/xvector_nnet_1a
kaldi_dir=/opt/kaldi
if [ $DataPre -eq 1 ]; then
        echo ==========================================
        echo "get utt2spk, DataPre start on" `date`
        echo ==========================================

        python make_data.py $wavdir $datadir
        utils/utt2spk_to_spk2utt.pl $datadir/utt2spk > $datadir/spk2utt || exit 1
        utils/spk2utt_to_utt2spk.pl $datadir/spk2utt > $datadir/utt2spk || exit 1

        echo ===== data preparatin finished successfully `date`==========
else
        echo ==========================================
        echo "get utt2spk, DataPre start on" `date`
        echo ==========================================
        python make_data_speaker.py $speakerPath $datadir
        $kaldi_dir/egs/timit/s5/utils/utt2spk_to_spk2utt.pl $datadir/utt2spk > $datadir/spk2utt || exit 1
        $kaldi_dir/egs/timit/s5/utils/spk2utt_to_utt2spk.pl $datadir/spk2utt > $datadir/utt2spk || exit 1

        echo ===== data preparatin finished successfully `date`==========
fi
if [ $FIXDATA -eq 1 ]; then
    echo ==========================================
        echo "sorted spk2utt ... : fix_data_dir start on" `date`
        echo ==========================================
    $kaldi_dir/egs/timit/s5/utils/fix_data_dir.sh $datadir
        echo ====== fix_data_dir finished successfully `date` ==========
fi


if [ $FeatureForMfcc -eq 1 ]; then
         echo ==========================================
         echo "FeatureForSpeaker start on" `date`
         echo ==========================================
        # Extract speaker features MFCC.
    steps/make_mfcc.sh --mfcc-config conf/mfcc.conf --nj 1 --cmd "$train_cmd" \
    $datadir $logdir/make_testmfcc $featdir/mfcc

    $kaldi_dir/egs/timit/s5/utils/fix_data_dir.sh $datadir
        echo ==== FeatureForSpeaker test successfully `date` ===========

fi
if [ $VAD -eq 1 ];then
         echo ==========================================
         echo "generate vad file in data/train, VAD start on" `date`
         echo ==========================================
        # Compute VAD decisions. These will be shared across both sets of features.
        sid/compute_vad_decision.sh --nj 1 --cmd "$train_cmd" \
    $datadir $logdir/make_testvad $featdir/vad

        utils/fix_data_dir.sh $datadir

echo ========== VAD test successfully `date` ===============
fi
if [ $EXTRACT -eq 1 ]; then
         echo ==========================================
         echo "EXTRACT start on" `date`
         echo ==========================================
        # Extract the xVectors
        sid/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd" --nj 1 \
    $nnet_dir $datadir $featdir/xvectors_test_mfcc

        echo ========= EXTRACT just for testing `date`=============
fi


