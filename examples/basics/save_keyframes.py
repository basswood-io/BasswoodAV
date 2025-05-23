import bv
import bv.datasets

content = bv.datasets.curated("pexels/time-lapse-video-of-night-sky-857195.mp4")
with bv.open(content) as container:
    # Signal that we only want to look at keyframes.
    stream = container.streams.video[0]
    stream.codec_context.skip_frame = "NONKEY"

    for i, frame in enumerate(container.decode(stream)):
        print(frame)
        frame.save(f"night-sky.{i:04d}.jpg")
