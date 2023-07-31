
import glob
from tqdm import tqdm

words_counter = {}
for dataset in glob.glob("/project/OML/chuber/2022/NMTGMinor/exp/ASR-NW/data/orig_en_cased/*.train.cased"):
    lines = [line for line in open(dataset)]
    for line in tqdm(lines):
        for r in [".",",",":",";","!","?"]:
            line = line.replace(r," ")
        while True:
            line2 = line.replace("  "," ")
            if len(line2)==len(line):
                break
            line = line2
        for word in line.strip().split():
            if word not in words_counter:
                words_counter[word] = 1
            else:
                words_counter[word] += 1

with open("training_data.txt","w") as f:
    for word, occ in words_counter.items():
        f.write(word+" "+str(occ)+"\n")
