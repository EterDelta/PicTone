import argparse
import os


class PicToneParser:
    """
    Argument parsing class for PicTone.
    Handles the command-line arguments to use the sampler.
    """

    def __init__(self):
        self.argument_parser = argparse.ArgumentParser()
        self._add_arguments()

    def _add_arguments(self):
        self.argument_parser.add_argument("-i", "--input", help="Path to the image file or folder to be processed.", type=self._input, required=True)
        self.argument_parser.add_argument("-o", "--output", help="Path to save the generated image file with encoded data.", type=str, required=True)
        self.argument_parser.add_argument("-r", "--rate", help="Sample rate for the output audio. Default: 44100", type=int, default=44100)
        self.argument_parser.add_argument("-d", "--depth", help="Bit depth for audio samples (8, 16, or 24). Default: 16", type=int, choices=[8, 16, 24], default=16)
        self.argument_parser.add_argument("-s", "--samples", help="Number of samples the input should be forced to last.", type=int, default=None)
        self.argument_parser.add_argument("-a", "--aspect", help="Whether to preserve the input aspect ratio.", type=bool, default=True)

    @staticmethod
    def _input(path):
        if os.path.isdir(path) or os.path.isfile(path):
            return path
        else:
            raise argparse.ArgumentTypeError(f"{path} is not a valid file or path")

    def parse_arguments(self) -> argparse.Namespace:
        args = self.argument_parser.parse_args()
        return args
