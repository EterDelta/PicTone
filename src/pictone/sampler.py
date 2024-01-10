from typing import Optional, Tuple

import numpy as np

from pictone.exception import InvalidThresholdError, UnsupportedDepthError


class EdgeSampler:
    """
    Main class for converting image data to audio.
    Processes data as edge samples, and packs them into stereo frames which can be
    further processed or played back as sound.
    """

    def __init__(self, thresh: int, byte_depth: int, samples_req: Optional[int] = None, keep_aspect: bool = True):
        if thresh < 0 or thresh > 255:
            raise InvalidThresholdError(thresh)
        self.threshold = thresh
        self.depth = byte_depth
        self.samples_req = samples_req
        self.keep_aspect = keep_aspect

    def sample_frames(self, data: np.ndarray) -> Tuple[bytearray, int]:
        """
        Samples the edge coordinates from the provided image data and converts them into audio frames.
        Returns a tuple of the frame data and the total sampled frames.
        """
        y_samples, x_samples = np.where(data > self.threshold)
        height, width = data.shape[:2]

        frame_count = len(x_samples)
        frames = bytearray()

        if frame_count > 0:
            if self.samples_req is not None:
                if frame_count < self.samples_req:
                    factor = self.samples_req // frame_count + 1
                    x_samples = np.repeat(x_samples, factor)[:self.samples_req]
                    y_samples = np.repeat(y_samples, factor)[:self.samples_req]
                else:
                    x_samples = x_samples[:self.samples_req]
                    y_samples = y_samples[:self.samples_req]

            sample_range = self._get_depth_range()

            x_samples = np.interp(x_samples,
                (0, width - 1) if self.keep_aspect else (x_samples.min(), x_samples.max()),
                sample_range
            )
            y_samples = np.interp(y_samples,
                (0, height - 1) if self.keep_aspect else (y_samples.min(), y_samples.max()),
                sample_range
            )

            frame_count = len(x_samples)

            for coord in zip(x_samples, y_samples):
                frame = self._pack_frame(coord)
                frames += frame
        else:
            if self.samples_req is not None:
                frame = self._pack_frame((0, 0))
                frames += b''.join([frame] * self.samples_req)
                frame_count = self.samples_req

        return frames, frame_count

    def _pack_frame(self, coord: Tuple[int, int]) -> bytes:
        """
        Packs a coordinate into an audio frame bytes with the adequate depth.
        """
        packed_coord = b''.join(int(sample).to_bytes(
            self.depth,
            byteorder='little',
            signed=False if self.depth == 1 else True
        ) for sample in coord)
        return packed_coord

    def _get_depth_range(self) -> Tuple[int, int]:
        """
        Gets the maximum positive and negative values for a sample of the specified depth.
        """
        if self.depth == 1:
            return 0, 255
        elif self.depth == 2:
            return -32768, 32767
        elif self.depth == 3:
            return -8388608, 8388607
        else:
            raise UnsupportedDepthError(self.depth * 8)
