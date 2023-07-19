
for file in `ls speech-datasets/earnings2*/media/*`
do
    python audioclient/client.py -i ffmpeg -f $file --asr-kv asr_server_en=http://192.168.0.60:5008/asr/infer/en,en --asr-kv version=offline --asr-kv segmenter=SHAS --ffmpeg-speed -1 --output-file ${file%.mp3}.whisper --no-textsegmenter --asr-kv max_segment_length=10
done

mkdir -p whisper_output_21
mv speech-datasets/earinings21/media/*.whisper whisper_output_21
mkdir -p whisper_output_22
mv speech-datasets/earinings22/media/*.whisper whisper_output_22
