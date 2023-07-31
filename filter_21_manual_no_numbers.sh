
cat aligned_21/*.new_words | cut -d"|" -f1 | sort | uniq -c | sed "s/^[[:space:]]*//g" | grep -vE "^1 " > aligned_21/all_new_words.txt

python filter_21_manual_no_numbers.py
