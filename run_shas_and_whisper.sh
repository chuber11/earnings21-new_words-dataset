
for year in 21 22
do
    mkdir -p whisper_output_$year
    for file in speech-datasets/earnings$year/media/*.mp3
    do
        id=`echo $file | rev | cut -d"/" -f1 | rev`

        if [ -f "whisper_output_$year/${id%.mp3}.whisper" ]; then
            continue
        fi

        python audioclient/client.py -i ffmpeg -f $file --asr-kv asr_server_en=http://192.168.0.60:5008/asr/infer/en,en --asr-kv version=offline --asr-kv segmenter=SHAS --ffmpeg-speed -1 --output-file whisper_output_$year/${id%.mp3}.whisper --no-textsegmenter --asr-kv max_segment_length=10
    done
done

