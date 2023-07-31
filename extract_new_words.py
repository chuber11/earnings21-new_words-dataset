
import glob
import json
import ast

categories_to_tags = {"ACRONYM": ["ABBREVIATION"],
                      "NAMED ENTITY": ["PERSON"],
                      "SPECIAL WORD": ["PRODUCT","EVENT","WORK_OF_ART","LAW","LOC","ORG"],
                      #"NUMBER": ["TIME","PERCENT","MONEY","QUANTITY","CARDINAL","YEAR","ALPHANUMERIC"] # TODO: uncomment if you also want to extract NUMBERS
                      }
tags_to_categories = {v2:k for k,v in categories_to_tags.items() for v2 in v}

for year in ["21"]: #,"22"]: # TODO: uncomment if you also want to extract for earnings22
    for nlp_file in sorted(glob.glob("speech-datasets/earnings"+year+"/transcripts/nlp_references/*.nlp")):
        id = nlp_file.split("/")[-1][:-len(".nlp")]
        print(id)

        if year == "21":
            wer_tag_file = "/".join(nlp_file.split("/")[:-2])+"/wer_tags/"+id+".wer_tag.json"
            wer_tag_info = json.load(open(wer_tag_file))
            #tags = set(v for id,d in wer_tag_info.items() for k,v in d.items())
            #print(tags)

        nlp_data = [line.strip().split("|") for line in open(nlp_file)][1:]
        for line in nlp_data:
            line[-1] = ast.literal_eval(line[-1])

        aligned_ref_file = "aligned_"+year+"/"+id+".ref"
        aligned_ref_data = [line.strip() for line in open(aligned_ref_file)]

        done_wer_tags = set()
        aligned_index = 0
        
        with open("aligned_"+year+"/"+id+".new_words", "w") as f:
            for i in range(len(nlp_data)):
                word = nlp_data[i][0] #+nlp_data[i][4]
                speaker = nlp_data[i][1]

                anz = 0
                while not word in aligned_ref_data[aligned_index]:
                    aligned_index += 1
                    anz += 1

                if year == "21":
                    wer_tags = nlp_data[i][-1]
                    wer_tags_to_catagories = {wer_tag: tags_to_categories[wer_tag_info[wer_tag]["entity_type"]] for wer_tag in wer_tags
                                              if wer_tag in wer_tag_info and wer_tag_info[wer_tag]["entity_type"] in tags_to_categories and
                                              wer_tag not in done_wer_tags}
                elif year == "22":
                    tags = nlp_data[i][-1]
                    wer_tags_to_catagories = {tag_[0]:tags_to_categories[tag_[1]] for tag in tags if (tag_ := tag.split(":")) and tag_[1] in tags_to_categories}

                if "ACRONYM" in wer_tags_to_catagories.values(): # remove other tags if ACRONYM
                    wer_tags_to_catagories = {k:v for k,v in wer_tags_to_catagories.items() if v == "ACRONYM"}

                if len(wer_tags_to_catagories)>1:
                    print(wer_tags_to_catagories)
                    continue

                for wer_tag, category in wer_tags_to_catagories.items():
                    new_word = word
                    j = i+1
                    while True:
                        if j == len(nlp_data) or wer_tag not in nlp_data[j][-1]:
                            if new_word.startswith("the "):
                                new_word = new_word[len("the "):]
                            f.write("|".join([str(x) for x in [new_word, speaker, category, aligned_index]])+"\n")
                            done_wer_tags.add(wer_tag)
                            break
                        word2 = nlp_data[j][0] #+nlp_data[j][4]
                        if not word2 in aligned_ref_data[aligned_index]:
                            print("WARNING: Not whole new word in one segment!")
                            done_wer_tags.add(wer_tag)
                            break
                        new_word += " "+word2
                        j += 1
