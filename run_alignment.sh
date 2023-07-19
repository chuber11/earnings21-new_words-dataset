
for year in 21 22
do
    mkdir -p aligned_$year
    for file in whisper_output_$year/*.whisper
    do
        id=`echo $file | rev | cut -d"/" -f1 | rev`

        if [ -f "aligned_$year/${id%.whisper}.ref" ]; then
            continue
        fi
        echo $file

        cat $file | tail -n+3 | head -n-1 | cut -d" " -f4- > __ref.txt

        line_count=$(wc -l < __ref.txt)
        if [ "$line_count" -eq 0 ]; then
            continue
        fi

        cat speech-datasets/earnings$year/transcripts/nlp_references/${id%.whisper}.nlp | tail -n+2 | awk -F"|" '{print $1$5}' | tr "\n" " " > __hypo.txt
        
        ./mwerSegmenter -mref __ref.txt -hypfile __hypo.txt -usecase 1
        mv __segments aligned_$year/${id%.whisper}.ref

        cat $file | tail -n+3 | head -n-1 | cut -d" " -f3 | sed 's/:$//g' | awk -v id="${id%.whisper}" -v year=$year -F"-" '{print id"_"NR" speech-datasets/earnings"year"/media/"id".mp3 "$1" "$2}' > aligned_$year/${id%.whisper}.seg.aligned
    done
done

rm __ref.txt
rm __hypo.txt
