"""
For each input format ansifier supports,
there must be a subclass of InputFormat,
and the INPUT_FORMATS map at the bottom of this file must map a string to it.

An InputFormat converts a filepath
into a list of PIL images
"""
# pyright: basic

# TODO
# * image URLs
# * youtube links


from abc import ABC, abstractmethod
from typing import BinaryIO

from PIL import Image
from PIL.ImageFile import ImageFile

from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB


class InputFormat(ABC):
    @staticmethod
    @abstractmethod
    def open(filepath: str) -> VideoCapture|ImageFile|None:
        pass

    @staticmethod
    @abstractmethod
    def yield_frames(rf: VideoCapture|ImageFile) -> ImageFile:
        """
        :return: one frame from the open input file per invocation until none are left
        """
        pass


class ImageInput(InputFormat):
    @staticmethod
    def open(filepath: str) -> VideoCapture|ImageFile|None: 
        return Image.open(filepath, 'r')

    @staticmethod
    def yield_frames(rf: ImageFile) -> ImageFile:  # pyright:ignore
        n_frames = getattr(rf, 'n_frames', 1)
        for frame_n in range(n_frames):
            rf.seek(frame_n)
            yield rf  # pyright:ignore


class VideoInput(InputFormat):
    @staticmethod
    def open(filepath: str) -> VideoCapture:
        return VideoCapture(filepath)


    @staticmethod
    def yield_frames(rf: VideoCapture) -> ImageFile:  # pyright:ignore
        success, bgr_frame = rf.read()
        while success:
            rgb_frame = cvtColor(bgr_frame, COLOR_BGR2RGB)
            frame = Image.fromarray(rgb_frame)
            yield frame  # pyright:ignore
            success, bgr_frame = rf.read()



INPUT_FORMATS = {
    'image': ImageInput,
    'video': VideoInput
}
