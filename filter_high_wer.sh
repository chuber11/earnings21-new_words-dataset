
for id in `cat aligned_21/alignment.log | grep -B1 -E ' (3|4|5)[0-9]\.' | grep whisper | cut -d"/" -f2 | cut -d"." -f1`; do echo $id && rm aligned_21/$id* ; done

