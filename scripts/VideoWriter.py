"""
Simple .mp4 video writer
"""
# ======================================================================================================================
import pathlib

import cv2
import numpy as np
import matplotlib.pyplot as plt


# ======================================================================================================================
class VideoWriter:
    """
    Thin wrapper around the OpenCV VideoWriter class for writing .mp4 video files
    """
    def __init__(self,
                 filename: str,
                 fps: float = 30,
                 isColor: bool = True):
        """
        Constructor

        Args:
            filename (str): filename The filename of the output video file, no extension
            fps: The frames per second of the video. Default 30
            isColor: Whether or not the video will contain color frames. Default True
        """
        p = pathlib.Path(filename)
        if not p.parent.exists():
            raise ValueError(f'Output directory does not exist\n{p.parent}')

        # Private Members:
        # The full filename for the output video file
        self._filename = str(p.with_suffix(''))
        # Shortened name for the plotting window
        self._name = p.name
        # The Frames per Second of the video
        self._fps = fps
        # Whether or not the video will contain color frames
        self._isColor = isColor
        # The OpenCV video writer object
        self._videoWriter = None

    # ==================================================================================================================
    def __del__(self) -> None:
        """
        Destructor
        """
        self.release()

    # ==================================================================================================================
    @property
    def filename(self) -> str:
        """
        Gets the video filename

        Returns:
            string path
        """
        return self._filename

    # ==================================================================================================================
    @property
    def fps(self) -> float:
        """
        Gets the video frame rate

        Returns:
            frame rate
        """
        return self._fps

    # ==================================================================================================================
    @property
    def isColor(self) -> bool:
        """
        Gets whether the video is in color or not

        Returns:
            bool true if in color
        """
        return self._isColor

    # ==================================================================================================================
    def addFrame(self,
                 frame: np.ndarray,
                 doPlot: bool = False) -> None:
        """
        Adds a frame to the video object

        Args:
            frame: A frame to add to the video
            doPlot: bool to plot the frame. Default False.

        Raises:
            RuntimeError: if the video has already been released
        """
        # Create if None
        if self._videoWriter is None:
            frameSize = (frame.shape[1], frame.shape[0])
            self._videoWriter = cv2.VideoWriter(filename=self._filename + '.avi',
                                                fourcc=cv2.VideoWriter_fourcc(*'MJPG'),
                                                fps=self._fps,
                                                frameSize=frameSize,
                                                isColor=self._isColor)

        if not self._videoWriter.isOpened():
            raise RuntimeError('VideoReader has already been released.')

        self._videoWriter.write(frame)

        if doPlot:
            cv2.imshow(self._name, frame)
            # needed for some reason so that the images will actually display while writing...
            if cv2.waitKey(1) & 0xFF == ord('q'):
                pass

    # ==================================================================================================================
    def addMatplotlibFigureHandle(self,
                                  fig: plt.Figure,
                                  doPlot=False) -> None:
        """
        Adds a matplotlib figure handle as a frame to the video object

        Args:
            fig: matplotlib figure handle
            doPlot: bool to plot the frame. Default False.

        Raises:
            RuntimeError: if the video has already been released
        """
        # extract the image info as a numpy array
        buf, [width, height] = fig.canvas.print_to_buffer()
        imageData = np.frombuffer(buffer=buf, dtype=np.uint8).reshape(height, width, 4)[:, :, :-1]  # strip alpha

        # numpy is [R, G, B, A] and opencv is [B, G, R, A] so
        # switch the color channels around
        red = imageData[:, :, 0]
        blue = imageData[:, :, 2]

        imageDataCv = imageData.copy()
        imageDataCv[:, :, 0] = blue
        imageDataCv[:, :, 2] = red

        # matplotlib is weird sometimes...
        if width != fig.canvas.width() or height != fig.canvas.height():
            imageResized = cv2.resize(src=imageDataCv,
                                      dsize=(fig.canvas.width(), fig.canvas.height()),
                                      interpolation=cv2.INTER_CUBIC)

            self.addFrame(frame=imageResized,
                          doPlot=doPlot)
        else:
            self.addFrame(frame=imageDataCv,
                          doPlot=doPlot)

    # ==================================================================================================================
    def release(self) -> None:
        """
        Releases the newly written video object
        """
        if self._videoWriter is not None and self._videoWriter.isOpened():
            self._videoWriter.release()
