import io
import math
from fractions import Fraction

import numpy as np
import pytest

import bv
from bv import AudioFrame, VideoFrame
from bv.audio.stream import AudioStream
from bv.video.stream import VideoStream

from .common import TestCase, fate_suite

WIDTH = 320
HEIGHT = 240
DURATION = 48


class TestBasicVideoEncoding(TestCase):
    def test_default_options(self) -> None:
        with bv.open(self.sandboxed("output.mov"), "w") as output:
            stream = output.add_stream("mpeg4")
            assert stream in output.streams.video
            assert stream.average_rate == Fraction(24, 1)
            assert stream.time_base is None

            # codec context properties
            assert stream.format.height == 480
            assert stream.format.name == "yuv420p"
            assert stream.format.width == 640
            assert stream.height == 480
            assert stream.pix_fmt == "yuv420p"
            assert stream.width == 640

    def test_encoding_with_pts(self) -> None:
        path = self.sandboxed("video_with_pts.mov")

        with bv.open(path, "w") as output:
            stream = output.add_stream("h264", 24)
            assert stream in output.streams.video
            stream.width = WIDTH
            stream.height = HEIGHT
            stream.pix_fmt = "yuv420p"

            for i in range(DURATION):
                frame = VideoFrame(WIDTH, HEIGHT, "rgb24")
                frame.pts = i * 2000
                frame.time_base = Fraction(1, 48000)

                for packet in stream.encode(frame):
                    assert packet.time_base == Fraction(1, 24)
                    output.mux(packet)

            for packet in stream.encode(None):
                assert packet.time_base == Fraction(1, 24)
                output.mux(packet)


class TestBasicAudioEncoding(TestCase):
    def test_default_options(self) -> None:
        with bv.open(self.sandboxed("output.mov"), "w") as output:
            stream = output.add_stream("mp2")
            assert stream in output.streams.audio
            assert stream.time_base is None

            # codec context properties
            assert stream.format.name == "s16"
            assert stream.sample_rate == 48000

    def test_transcode(self) -> None:
        path = self.sandboxed("audio_transcode.mov")

        with bv.open(path, "w") as output:
            output.metadata["title"] = "container"
            output.metadata["key"] = "value"

            sample_rate = 48000
            channel_layout = "stereo"
            sample_fmt = "s16"

            stream = output.add_stream("mp2", sample_rate)
            assert stream in output.streams.audio

            ctx = stream.codec_context
            ctx.sample_rate = sample_rate
            stream.format = sample_fmt
            ctx.layout = channel_layout

            with bv.open(
                fate_suite("audio-reference/chorusnoise_2ch_44kHz_s16.wav")
            ) as src:
                for frame in src.decode(audio=0):
                    for packet in stream.encode(frame):
                        output.mux(packet)

            for packet in stream.encode(None):
                output.mux(packet)

        with bv.open(path) as container:
            assert len(container.streams) == 1
            assert container.metadata.get("title") == "container"
            assert container.metadata.get("key") is None

            assert isinstance(container.streams[0], AudioStream)
            stream = container.streams[0]

            # codec context properties
            assert stream.format.name == "s16p"
            assert stream.sample_rate == sample_rate


class TestSubtitleEncoding:
    def test_subtitle_muxing(self) -> None:
        input_ = bv.open(fate_suite("sub/MovText_capability_tester.mp4"))
        in_stream = input_.streams.subtitles[0]

        output_bytes = io.BytesIO()
        output = bv.open(output_bytes, "w", format="mp4")

        out_stream = output.add_stream_from_template(in_stream)

        for packet in input_.demux(in_stream):
            if packet.dts is None:
                continue
            packet.stream = out_stream
            output.mux(packet)

        output.close()
        output_bytes.seek(0)
        assert output_bytes.getvalue().startswith(
            b"\x00\x00\x00\x1cftypisom\x00\x00\x02\x00isomiso2mp41\x00\x00\x00\x08free"
        )


class TestEncodeStreamSemantics(TestCase):
    def test_stream_index(self) -> None:
        with bv.open(self.sandboxed("output.mov"), "w") as output:
            vstream = output.add_stream("mpeg4", 24)
            assert vstream in output.streams.video
            vstream.pix_fmt = "yuv420p"
            vstream.width = 320
            vstream.height = 240

            astream = output.add_stream("mp2", 48000)
            assert astream in output.streams.audio
            astream.layout = "stereo"
            astream.format = "s16"

            assert vstream.index == 0
            assert astream.index == 1

            vframe = VideoFrame(320, 240, "yuv420p")
            vpacket = vstream.encode(vframe)[0]

            assert vpacket.stream is vstream
            assert vpacket.stream_index == 0

            for i in range(10):
                if astream.frame_size != 0:
                    frame_size = astream.frame_size
                else:
                    # decoder didn't indicate constant frame size
                    frame_size = 1000
                aframe = AudioFrame("s16", "stereo", samples=frame_size)
                aframe.sample_rate = 48000
                apackets = astream.encode(aframe)
                if apackets:
                    apacket = apackets[0]
                    break

            assert apacket.stream is astream
            assert apacket.stream_index == 1

    def test_stream_audio_resample(self) -> None:
        with bv.open(self.sandboxed("output.mov"), "w") as output:
            vstream = output.add_stream("mpeg4", 24)
            vstream.pix_fmt = "yuv420p"
            vstream.width = 320
            vstream.height = 240

            astream = output.add_stream("aac", sample_rate=8000, layout="mono")
            frame_size = 512

            pts_expected = [-1024, 0, 512, 1024, 1536, 2048, 2560]
            pts = 0
            for i in range(15):
                aframe = AudioFrame("s16", "mono", samples=frame_size)
                aframe.sample_rate = 8000
                aframe.time_base = Fraction(1, 1000)
                aframe.pts = pts
                aframe.dts = pts
                pts += 32
                apackets = astream.encode(aframe)
                if apackets:
                    apacket = apackets[0]
                    assert apacket.pts == pts_expected.pop(0)
                    assert apacket.time_base == Fraction(1, 8000)

            apackets = astream.encode(None)
            if apackets:
                apacket = apackets[0]
                assert apacket.pts == pts_expected.pop(0)
                assert apacket.time_base == Fraction(1, 8000)

    def test_set_id_and_time_base(self) -> None:
        with bv.open(self.sandboxed("output.mov"), "w") as output:
            stream = output.add_stream("mp2")
            assert stream in output.streams.audio

            # set id
            assert stream.id == 0
            stream.id = 1
            assert stream.id == 1

            # set time_base
            assert stream.time_base is None
            stream.time_base = Fraction(1, 48000)
            assert stream.time_base == Fraction(1, 48000)


def encode_file_with_max_b_frames(max_b_frames: int) -> io.BytesIO:
    """
    Create an encoded video file (or file-like object) with the given
    maximum run of B frames.

    max_b_frames: non-negative integer which is the maximum allowed run
        of consecutive B frames.

    Returns: a file-like object.
    """
    # Create a video file that is entirely arbitrary, but with the passed
    # max_b_frames parameter.
    file = io.BytesIO()
    container = bv.open(file, mode="w", format="mp4")
    stream = container.add_stream("h264", rate=30)
    stream.width = 640
    stream.height = 480
    stream.pix_fmt = "yuv420p"
    stream.codec_context.gop_size = 15
    stream.codec_context.max_b_frames = max_b_frames

    for i in range(50):
        array = np.empty((stream.height, stream.width, 3), dtype=np.uint8)
        # This appears to hit a complexity "sweet spot" that makes the codec
        # want to use B frames.
        array[:, :] = (i, 0, 255 - i)
        frame = bv.VideoFrame.from_ndarray(array, format="rgb24")
        for packet in stream.encode(frame):
            container.mux(packet)

    for packet in stream.encode():
        container.mux(packet)

    container.close()
    file.seek(0)

    return file


def max_b_frame_run_in_file(file: io.BytesIO) -> int:
    """
    Count the maximum run of B frames in a file (or file-like object).

    file: the file or file-like object in which to count the maximum run
        of B frames. The file should contain just one video stream.

    Returns: non-negative integer which is the maximum B frame run length.
    """
    container = bv.open(file, "r")
    stream = container.streams.video[0]

    max_b_frame_run = 0
    b_frame_run = 0
    for frame in container.decode(stream):
        if frame.pict_type == bv.video.frame.PictureType.B:
            b_frame_run += 1
        else:
            max_b_frame_run = max(max_b_frame_run, b_frame_run)
            b_frame_run = 0

    # Outside chance that the longest run was at the end of the file.
    max_b_frame_run = max(max_b_frame_run, b_frame_run)

    container.close()

    return max_b_frame_run


class TestMaxBFrameEncoding(TestCase):
    def test_max_b_frames(self) -> None:
        """
        Test that we never get longer runs of B frames than we asked for with
        the max_b_frames property.
        """
        for max_b_frames in range(4):
            file = encode_file_with_max_b_frames(max_b_frames)
            actual_max_b_frames = max_b_frame_run_in_file(file)
            assert actual_max_b_frames <= max_b_frames


def encode_frames_with_qminmax(frames: list, shape: tuple, qminmax: tuple) -> int:
    """
    Encode a video with the given quantiser limits, and return how many enocded
    bytes we made in total.

    frames: the frames to encode
    shape: the (numpy) shape of the video frames
    qminmax: two integers with 1 <= qmin <= 31 giving the min and max quantiser.

    Returns: total length of the encoded bytes.
    """

    if bv.codec.Codec("h264", "w").name != "libx264":
        pytest.skip()

    file = io.BytesIO()
    container = bv.open(file, mode="w", format="mp4")
    stream = container.add_stream("h264", rate=30)
    stream.height, stream.width, _ = shape
    stream.pix_fmt = "yuv420p"
    stream.codec_context.gop_size = 15
    stream.codec_context.qmin, stream.codec_context.qmax = qminmax

    bytes_encoded = 0
    for frame in frames:
        for packet in stream.encode(frame):
            bytes_encoded += packet.size

    for packet in stream.encode():
        bytes_encoded += packet.size

    container.close()

    return bytes_encoded


class TestQminQmaxEncoding(TestCase):
    def test_qmin_qmax(self) -> None:
        """
        Test that we can set the min and max quantisers, and the encoder is reacting
        correctly to them.

        Can't see a way to get hold of the quantisers in a decoded video, so instead
        we'll encode the same frames with decreasing quantisers, and check that the
        file size increases (by a noticeable factor) each time.
        """
        # Make a random - but repeatable - 10 frame video sequence.
        np.random.seed(0)
        frames = []
        shape = (480, 640, 3)
        for _ in range(10):
            frames.append(
                bv.VideoFrame.from_ndarray(
                    np.random.randint(0, 256, shape, dtype=np.uint8), format="rgb24"
                )
            )

        # Get the size of the encoded output for different quantisers.
        quantisers = ((31, 31), (15, 15), (1, 1))
        sizes = [
            encode_frames_with_qminmax(frames, shape, qminmax) for qminmax in quantisers
        ]

        factor = 1.3  # insist at least 30% larger each time
        assert all(small * factor < large for small, large in zip(sizes, sizes[1:]))


class TestProfiles(TestCase):
    def test_profiles(self) -> None:
        """
        Test that we can set different encoder profiles.
        """
        # Let's try a video and an audio codec.
        file = io.BytesIO()
        codecs = (
            ("h264", 30),
            ("aac", 48000),
        )

        for codec_name, rate in codecs:
            print("Testing:", codec_name)
            container = bv.open(file, mode="w", format="mp4")
            stream = container.add_stream(codec_name, rate=rate)
            assert len(stream.profiles) >= 1  # check that we're testing something!

            # It should be enough to test setting and retrieving the code. That means
            # libav has recognised the profile and set it correctly.
            for profile in stream.profiles:
                stream.profile = profile
                print("Set", profile, "got", stream.profile)
                assert stream.profile == profile
