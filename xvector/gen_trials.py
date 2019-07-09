import os
import sys
wav_dir = sys.argv[1]
save_name = sys.argv[2]

# wav_dir/spk/*.wav

def func_gen1(wav_dir):
#python gen_trials.py ../../vc_feature/vctk/test-0601/unseen-libri/wav16-baseline30/
    spk_list = os.listdir(wav_dir)
    print(spk_list)
    for fi in os.listdir(wav_dir):
        f1_path = os.path.join(wav_dir, fi)
        for f1 in os.listdir(f1_path):
            wav_id = f1.split('.wav')[0]
            utt_id = fi +'-'+ wav_id
            #print(utt_id, spk)
            for i in range(len(spk_list)):
                print(spk_list[i], wav_id[:3])
                spk = spk_list[i]
                print('spk,wav',spk[-3:], wav_id[:3])
                #if (spk[-3:] == wav_id[:3]):
                #    os.system('echo %s %s target >> trials' %(spk_list[i], utt_id))
                #else:
                #    os.system('echo %s %s nontarget >> trials' %(spk_list[i], utt_id))
def func_gen2(wav_dir, save_name):
    spk_list = os.listdir(wav_dir)
    for f1 in os.listdir(wav_dir):
        wav_path = os.path.join(wav_dir, f1, 'wav')
        for fi in os.listdir(wav_path):
            wav_name = os.path.join(wav_path, fi)
            print('f1',f1)
            f1_spk = f1.split('-',1)[1]
            fi_name = fi.split('.wav')[0]
            utt_id = f1_spk +'-'+ fi_name
            print('f1_spk, utt_id', f1_spk, utt_id)
            os.system('echo %s %s >> %s'%(wav_name, f1_spk, save_name))
            for i in range(len(spk_list)):
                spk = spk_list[i]
                print('spk', spk)
                spk = spk.split('-',1)[1]
                print('spk',spk)
                if (f1_spk == spk):
                    os.system('echo %s %s target >> trials' %(spk, utt_id))
                else:  os.system('echo %s %s nontarget >> trials' %(spk, utt_id))

def main():
    #func_gen1(wav_dir)
    func_gen2(wav_dir, save_name)


if __name__ == '__main__':
    main()
