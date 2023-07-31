
1) run_shas_and_whisper.sh runs SHAS and Whisper on all talks (using the KIT Lecture Translator) and saves the transcript to whisper_output_2*/*.whisper
2) run_alignment.sh alignes the given nlp transcript with the Whisper output and saves the aligments in aligned_2*/*.seg.aligned and aligned_2*/*.ref (pipe output to aligned_21/alignment.log)
2.5) Run filter_high_wer.sh (filters WER >= 30%)
3) extract_new_words.py extracts the new words into catagories and saves this in aligned_2*/*.new_words
4) filter_21_manual_no_numbers.sh manually filters the new words (occuring two or more times) and saves the output to aligned_21/all_new_words_filtered.txt (evaluate_after_learning.txt and replacements.txt have been created during this manual filtering)
5) Create a training_data.txt file containing the word and number of occurances (e.g. with count_training_data.py)
6) Run extract_new_words_dataset.py to generate nw dataset

