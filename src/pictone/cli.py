import argparse
import os.path
import wave

import cv2

from pictone.exception import SamplerError
from pictone.parser import PicToneParser
from pictone.sampler import EdgeSampler


def entry():
    parser = PicToneParser()

    try:
        args = parser.parse_arguments()

        input_path = args.input
        output_path = args.output
        depth_width = args.depth // 8

        frames = bytearray()
        frame_count = 0

        sampler = EdgeSampler(0, depth_width, args.samples, args.aspect)

        if os.path.isfile(input_path):
            img = cv2.imread(input_path, 0)
            img_edges = cv2.Canny(img, 100, 200)

            frames, frame_count = sampler.sample_frames(img_edges)

        elif os.path.isdir(input_path):
            input_files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]

            for file in input_files:
                img = cv2.imread(os.path.join(input_path, file))
                img_edges = cv2.Canny(img, 100, 200)
                out_frames, out_count = sampler.sample_frames(img_edges)
                frames += out_frames
                frame_count += out_count

        with wave.open(output_path, 'w') as wav_file:
            n_channels = 2
            sample_width = depth_width
            sample_rate = args.rate
            n_frames = frame_count
            comp_type = 'NONE'
            comp_name = "not compressed"

            wav_file.setparams((n_channels, sample_width, sample_rate, n_frames, comp_type, comp_name))
            wav_file.writeframesraw(frames)

    except argparse.ArgumentTypeError as e:
        print(e)
        parser.argument_parser.print_help()
    except SamplerError as e:
        print(e)
    except Exception as e:
        print(f"An error has occurred during file handling: {e}")
