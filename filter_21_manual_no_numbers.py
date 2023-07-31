
from tqdm import tqdm

with open("aligned_21/all_new_words_filtered.txt","w") as f:
    lines = [line.strip() for line in open("aligned_21/all_new_words.txt")]
    for i,line in enumerate(tqdm(lines)):
        print("CONTEXT:")
        for x in lines[max(0,i-10):i+10]:
            print("    ",x)
        print("WORD:")
        print("    ",lines[i])
        while True:
            x = input("Use this word? ")
            if x == "1":
                f.write(line.split()[1]+"\n")
                break
            elif x == "0":
                break
