from transformers import AutoProcessor, SeamlessM4Tv2Model
import torchaudio
import scipy
import argparse

def main(input_file: str, output_file: str, language: str) -> None:
    processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
    model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")

    # from text
    #text_inputs = processor(text = "Hello, my dog is cute", src_lang="eng", return_tensors="pt")
    #audio_array_from_text = model.generate(**text_inputs, tgt_lang="rus")[0].cpu().numpy().squeeze()

    # from audio
    audio, orig_freq = torchaudio.load(input_file)
    audio =  torchaudio.functional.resample(audio, orig_freq=orig_freq, new_freq=16_000) # must be a 16 kHz waveform array
    audio_inputs = processor(audios=audio, return_tensors="pt")
    audio_array_from_audio = model.generate(**audio_inputs, tgt_lang=language)[0].cpu().numpy().squeeze()

    sample_rate = model.config.sampling_rate
    scipy.io.wavfile.write(output_file, rate=sample_rate, data=audio_array_from_audio)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Wrapper for Facebook Seamless.")
    
    parser.add_argument('--input_file', type=str, required=True, help="Path to the input file")
    parser.add_argument('--output_file', type=str, required=True, help="Path to the output file")
    parser.add_argument('--language', type=str, required=True, help="Traget language code for translation")
    args = parser.parse_args()

    main(args.input_file, args.output_file, args.language)

