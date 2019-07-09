import os
import time
import shutil


def get_scores(model_list, utt_dir):
    for m in list(model_list):
        wav_dir = os.path.join(utt_dir, m)
        gen_txt(wav_dir)

#step1:gen_txt
def gen_txt(lpc_dir):
    a = lpc_dir.split('/')
    txt_name = a[-3]+'_'+a[-2]+'_'+a[-1]+'.txt'
    print('txt_name',txt_name)
    os.system('python gen_trials.py %s %s'%(lpc_dir, txt_name))
    os.system('bash test.sh %s 2'%txt_name)
    src_trials = os.path.join('/home/zhangying09/.jupyter/ivector-xvector/eer','trials')
    tar_trials = os.path.join('/home/zhangying09/.jupyter/ivector-xvector/eer/data/test','trials')
    shutil.move(src_trials, tar_trials)
    os.system('bash plda_scoring.sh %s'%txt_name)

def main():
    #model_list = ['m60','m65','m70','m75','m80','m85','m90','m95','m100','m105','m110']
    while(1):
        time.sleep(60)
        print ("Current : %s" % time.ctime())
        if os.path.exists('begin'):
            model_list = ['m35', 'm40','m45', 'm50']
            utt_dir = '/home/zhangying09/.jupyter/voice-conversion-vector/vc-ivec/vctk89-100/vctk100-ivec-whole/test_0608/ivec100-whole/utt10/'

            get_scores(model_list, utt_dir)

            utt_dir = '/home/zhangying09/.jupyter/voice-conversion-vector/vc-ivec/vctk89-100/vctk100-ivec-whole/test_0608/ivec100-whole/utt01'
            get_scores(model_list, utt_dir)

            #utt_dir = '/home/zhangying09/.jupyter/voice-conversion-vector/vc-xvec/vctk89-100/vctk100-xvec-whole/test_0608/xvec100-whole/utt05'
            utt_dir = '/home/zhangying09/.jupyter/voice-conversion-vector/vc-ivec/vctk89-100/vctk100-ivec-whole/test_0608/ivec100-whole/utt05'
            get_scores(model_list, utt_dir)
            break
    #utt_dir = '/home/zhangying09/.jupyter/voice-conversion-vector/vc-xvec/vctk89-100/vctk100-xvec-whole/test_0608/xvec100-whole/utt30'
    #get_scores(model_list, utt_dir)

if __name__ == '__main__':
    main()
