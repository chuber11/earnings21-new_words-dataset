
import sys
import glob
import random

replacements = {tmp[0]:tmp[1] for line in open("aligned_21/replacements.txt") if line[0] != "#" and (tmp := line.strip().split("|"))}
filtering = set([line.strip() for line in open("aligned_21/all_new_words_filtered.txt") if line[0] != "#"])
filtering2 = set(tmp[0].lower() for line in open("training_data.txt") if (tmp := line.strip().split()))
evaluate_after_learning = {tmp[0]:tmp[1] for line in open("aligned_21/evaluate_after_learning.txt") if line[0] != "#" and (tmp := line.strip().split("|"))}

counter_word = {} # map new word to ((file,speaker_id),category,line_id)
for f in glob.glob("aligned_21/*.new_words"):
    if f.startswith("aligned_21/nw"):
        continue

    for line in open(f):
        line = line.strip().split("|")
        word = line[0]
        speaker = line[1]
        cat = line[2]
        line_id = line[3]

        if not word in filtering or word.lower() in filtering2:
            continue
        if word in replacements:
            word = replacements[word]
        if word in evaluate_after_learning and evaluate_after_learning[word] in counter_word:
            continue

        if word not in counter_word:
            counter_word[word] = [[(f,speaker),cat,line_id]]
        else:
            counter_word[word].append([(f,speaker),cat,line_id])

counter_word = {word:c for word,c in counter_word.items() if len(c)>=2} # filter for >=2 occurances

word_to_cats = {word:set(cat for _,cat,_ in s) for word,s in counter_word.items()}

word_to_cats = {k:v if not "ACRONYM" in v else set(["ACRONYM"]) for k,v in word_to_cats.items()} # if it has multiple labels including acronym it is an acronym
word_to_cats = {k:v if not "NAMED ENTITY" in v else set(["NAMED ENTITY"]) for k,v in word_to_cats.items()} # same for named entity

if any(len(v)>1 for k,v in word_to_cats.items()):
    print([v for k,v in word_to_cats.items() if len(v)>1])
    print("ERROR: Found multiple category labels for at least one word")
    sys.exit()

for word,s in counter_word.items():
    for i in range(len(s)):
        cat = list(word_to_cats[word])[0]
        s[i][1] = cat

segments_to_references = {}
for x in counter_word.values():
    for (f,_),_,line_id in x:
        for i,line in enumerate(open(f[:-len("new_words")]+"ref")):
            if int(line_id) == i:
                ref = line.strip()
                for s,r in replacements.items():
                    ref = ref.replace(s,r)
                segments_to_references[(f,line_id)] = ref

counter_word = list(counter_word.items())
counter_word.sort(key=lambda item: len(item[1])) # first choose segments of words with few occurances

used_segments = set()
used_new_words = set()
used_references = set()
data = [[] for _ in range(6)]
no2speakers = 0
for word_id, (word, s) in enumerate(counter_word):
    speakers = {}
    for s_id, cat, line_id in s:
        if not s_id in speakers:
            speakers[s_id] = [line_id]
        else:
            speakers[s_id].append(line_id)

    speakers = list(speakers.items())
    speakers.sort(key=lambda item: len(item[1])) # choose speaker which has spoken the new word the fewest times as test (if possible)

    index_set = 0
    num_added = 0
    new_references = set()
    for index_speaker, (s_id, line_ids) in enumerate(speakers):
        for line_id in line_ids:
            file = s_id[0]
            used_segment = (file,line_id)

            # make sure every segment is only used once
            # make sure a used new word does not occur in samples of other new words
            if used_segment not in used_segments and \
                not any(new_word in segments_to_references[used_segment] for new_word in used_new_words) and \
                not any(word in reference for reference in used_references):

                used_segments.add(used_segment)
                new_references.add(segments_to_references[used_segment])
                if index_set == 0:
                    used_segment_0 = used_segment
                num_added += 1

                data[index_set].append((file,line_id,word,word_id,cat))

                if index_set < 5:
                    index_set += 1
                    if index_set == 1:
                        if index_speaker == len(speakers) - 1:
                            no2speakers += 1
                        else:
                            break

    if num_added == 0:
        pass #print("FOUND NONE")
    elif num_added == 1:
        data[0] = data[0][:-1]
        used_segments.remove(used_segment_0)
        #print("FOUND NO 2ND")
    else:
        used_new_words.add(word)
        for reference in new_references:
            used_references.add(reference)

print("No two speakers for",no2speakers,"samples!")

cat_to_indices = {} # maps categories to word indices where the word is of the corresponding category
for s in data[0]:
    cat = s[-1]
    i = s[3]
    if cat not in cat_to_indices:
        cat_to_indices[cat] = [i]
    else:
        cat_to_indices[cat].append(i)

percent_devset = 15
random.seed(42)

indices_dev = set(index for cat,indices in cat_to_indices.items() for index in random.sample(indices,int(len(indices)*percent_devset/100))) # randomly choose percent_devset % of each category for dev set

set_names = ["test"]+["train."+str(i+1) for i in range(5)]

for split in ["dev","test"]: # write out files
    for set,d in zip(set_names,data):
        with open("aligned_21/nw."+split+"."+set+".seg.aligned","w") as f, open("aligned_21/nw."+split+"."+set+".ref","w") as f2, open("aligned_21/nw."+split+"."+set+".new_words","w") as f3:
            for file, line_index, new_word, new_word_index, cat in d:
                if (new_word_index in indices_dev) ^ (split != "dev"):
                    for i,line in enumerate(open(file[:-len("new_words")]+"seg.aligned")):
                        if str(i) == line_index:
                            break
                    f.write(line)
                    for i,line in enumerate(open(file[:-len("new_words")]+"ref")):
                        if str(i) == line_index:
                            break
                    for s,r in replacements.items():
                        line = line.replace(s,r)
                    f2.write(line)
                    f3.write(new_word+"|"+cat+"\n")
