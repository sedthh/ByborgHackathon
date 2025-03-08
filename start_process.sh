#!/bin/bash
# For just in case, run as root (because conda command)
#TODO Later need to resolve this issue

# Check if a filename was provided
if [ -z "$1" ]; then
    echo "Required parameter: $0 <filename.mp4>"
    exit 1
fi

# Input and output directory
data_dir="$(pwd)/data"

# Check if the data directory exists
if [ ! -d "$data_dir" ]; then
    echo "Error: The data directory is not exist!"
    exit 1
fi

# Input file in the data directory
input_file="$data_dir/$1"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: The specified file does not exist in the data directory!"
    exit 1
fi

# Extract filename without extension
filename="${1%.mp4}"

# Output file sound file (mp3)
output_mp3_file="$data_dir/${filename}.mp3"

#STEP 1
# Run the ffmpg
ffmpeg -i "$input_file" -vn -acodec mp3 "$output_mp3_file"

echo "Sound track conversion completed. Created in the data directory: $output_mp3_file"

#STEP 2

# Output first mask file (jpg)
input_first_mask_file="$data_dir/${filename}.jpg"
# Run the MatAnyone
source MatAnyone/myenv/bin/activate

python MatAnyone/inference_matanyone.py -i "$input_file" -m "$input_first_mask_file"

cp "./MatAnyone/results/${filename}_pha.mp4" "../data/${filename}_pha.mp4"
cp "./MatAnyone/results/${filename}_fgr.mp4" "../data/${filename}_fgr.mp4"
deactivate

#STEP 3
# Create Depth fast grey layer
source RollingDepth/myvenv/bin/activate

python3 RollingDepth/run_video.py -i "$input_file" -o ../data/depth_fast_outputs -p fast --verbose

cp "data/depth_fast_outputs/${filename}_Greys_r.mp4" "data/${filename}_Greys_r.mp4"
deactivate

#STEP 4
# Seamless
source seamless_huggingface/myvenv/bin/activate

python3 seamless_huggingface/seamless_workaround.py --input_file "$output_mp3_file" --output_file "../data/${filename}_fra.mp3" --language fra
python3 seamless_huggingface/seamless_workaround.py --input_file "$output_mp3_file" --output_file "../data/${filename}_deu.mp3" --language deu
deactivate

#STEP 5
# OpenVoice

conda init
conda activate openvoice

python3 OpenVoice/openvoice.py --source_speaker "../data/${filename}_deu.mp3" --reference_speaker "$output_mp3_file" --save_path "../data/${filename}_deu-in-my-voice.wav"
python3 OpenVoice/openvoice.py --source_speaker "../data/${filename}_fra.mp3" --reference_speaker "$output_mp3_file" --save_path "../data/${filename}_fra-in-my-voice.wav"

conda deactivate

echo "All output files created."
