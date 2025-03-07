import os
import torch
from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter
import argparse


def main(source_speaker: str, reference_speaker: str, save_path: str) -> None:
    ckpt_base = 'checkpoints/base_speakers/EN'
    ckpt_converter = 'checkpoints/converter'

    base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device="cuda:0")
    base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')

    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device="cuda:0")
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')
    
    source_se = torch.load(f'{ckpt_base}/en_default_se.pth').to("cuda:0")
    target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, target_dir='processed', vad=True)
    
    # Run the tone color converter
    encode_message = "@MyShell"
    tone_color_converter.convert(
        audio_src_path=source_speaker, 
        src_se=source_se, 
        tgt_se=target_se, 
        output_path=save_path,
        message=encode_message)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Wrapper for Facebook Seamless.")
    
    parser.add_argument('--source_speaker', type=str, required=True, help="Text to generate")
    parser.add_argument('--reference_speaker', type=str, required=True, help="Path to the reference speaker wav file")
    parser.add_argument('--save_path', type=str, required=True, help="Path to the output wav file")
    args = parser.parse_args()

    assert torch.cuda.is_available(), "NO CUDA"
    
    main(args.source_speaker, args.reference_speaker, args.save_path)