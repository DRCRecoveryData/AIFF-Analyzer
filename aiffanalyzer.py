import os
import struct

class AIFFAnalyzer:
    def analyze_aiff_header(self, path):
        try:
            with open(path, "rb") as file:
                form, size = struct.unpack(">4sI", file.read(8))
                if form != b"FORM":
                    print("Error: Not a valid AIFF file.")
                    return

                format_name = file.read(4).decode("ascii")
                print("Displaying AIFF File Header Data for File", os.path.basename(path))
                print("Number of Bytes:", os.path.getsize(path))
                print("Reading AIFF Header...")
                print("Chunk Size:", size)
                print("Format:", format_name)

                while True:
                    chunk_name, chunk_size = struct.unpack(">4sI", file.read(8))
                    if chunk_name == b"COMM":
                        self.analyze_comm_chunk(file, chunk_size)
                    elif chunk_name == b"SSND":
                        self.analyze_ssnd_chunk(file, chunk_size)
                    else:
                        file.seek(chunk_size, 1)
        except FileNotFoundError:
            print("Error: File not found.")

    def analyze_comm_chunk(self, file, chunk_size):
        num_channels, num_frames, bits_per_sample = struct.unpack(">2Hh", file.read(8))
        print("Reading COMM chunk (size: {})".format(chunk_size))
        print("Number of Channels:", num_channels)
        print("Number of Frames:", num_frames)
        print("Bits per Sample:", bits_per_sample)
        sample_rate = struct.unpack(">Q", file.read(8))[0] / 65536
        print("Sample Rate:", sample_rate)

    def analyze_ssnd_chunk(self, file, chunk_size):
        print("Reading SSND chunk (size: {}).".format(chunk_size))
        offset, block_size = struct.unpack(">2I", file.read(8))
        print("Offset:", offset)
        print("Block Size:", block_size)

# Prompting user for file path
file_path = input("Enter the path of the AIFF file to analyze: ")
analyzer = AIFFAnalyzer()
analyzer.analyze_aiff_header(file_path)
