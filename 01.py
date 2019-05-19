import os
import sys

wav_dir = sys.argv[1]

for f1 in os.listdir(wav_dir):
    f1_path = os.path.join(wav_dir, f1)
    print("f1_path", f1_path)
    print('f1-lable', f1[1:4])

    for fi in os.listdir(f1_path):
        if fi.endswith('.wav'):
            utt_id = fi.split('.wav')[0]
            wav_path = os.path.join(f1_path, fi)
            label = f1[1:4]

            os.system('echo %s %s >> wav.scp' %(utt_id, wav_path)
            os.system('echo %s %s >> utt2spk' %(utt_id, label))
