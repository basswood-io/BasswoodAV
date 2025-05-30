import time

import bv
import bv.datasets

print("Decoding with default (slice) threading...")

container = bv.open(
    bv.datasets.curated("pexels/time-lapse-video-of-night-sky-857195.mp4")
)

start_time = time.time()
for packet in container.demux():
    print(packet)
    for frame in packet.decode():
        print(frame)

default_time = time.time() - start_time
container.close()


print("Decoding with auto threading...")

container = bv.open(
    bv.datasets.curated("pexels/time-lapse-video-of-night-sky-857195.mp4")
)

# !!! This is the only difference.
container.streams.video[0].thread_type = "AUTO"

start_time = time.time()
for packet in container.demux():
    print(packet)
    for frame in packet.decode():
        print(frame)

auto_time = time.time() - start_time
container.close()


print(f"Decoded with default threading in {default_time:.2f}s.")
print(f"Decoded with auto threading in {auto_time:.2f}s.")
