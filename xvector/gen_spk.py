import os
import sys

wav_dir = sys.argv[1]
save_path = sys.argv[2]
function =sys.argv[3]

def wav_with_name(wav_dir, save_path):
    for wav in os.listdir(wav_dir):
        spk = wav[:4]
        wav_name = wav.split('.wav')[0]
        utt_id = spk +'-'+ wav_name
        wav_path = os.path.join(wav_dir, wav)
        print('spk,wav_path', spk, wav_path)
        print('utt_id', utt_id)
        os.system('echo p226 %s nontarget >> trials'%(utt_id))
        #os.system('echo %s %s target >> trials'%(spk, utt_id))
        #os.system('echo %s %s >> %s'%(wav_path, spk, save_path))


def wav_no_name(wav_dir, save_path):
    for wav in os.listdir(wav_dir):
        spk = wav_dir.split('/')[-2]
        spk = spk.split('-',1)[0]
        wav_name = wav.split('.wav')[0]
        utt_id = spk +'-'+ wav_name
        wav_path = os.path.join(wav_dir, wav)
        print(spk, wav_path)
        print('utt_id', utt_id)
        #os.system('echo %s %s target >> trials'%(spk, utt_id))
        #os.system('echo %s %s >> %s'%(wav_path, spk, save_path))
        os.system('echo p226 %s nontarget >> trials'%(utt_id))
        
def negative_sample(wav_dir, spk, save_path):
    for wav in os.listdir(wav_dir):
        wav_name = wav.split('.wav')[0]
        utt_id = spk +'-'+ wav_name
        wav_path = os.path.join(wav_dir, wav)
        print(spk, wav_path)
        os.system('echo p303 %s nontarget >> trials'%(utt_id))

if __name__=="__main__":
    if(function=='a'):
        wav_with_name(wav_dir, save_path)
    elif(function == 'b'):
        wav_no_name(wav_dir, save_path)
    elif(function == 'c'):
        negative_sample(wav_dir, spk, save_path)
