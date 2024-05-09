import os
import struct

class AIFFAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path

    def analyze_aiff_header(self):
        try:
            with open(self.file_path, "rb") as file:
                form, size = struct.unpack(">4sI", file.read(8))
                if form != b"FORM":
                    raise ValueError("Not a valid AIFF file.")

                format_name = file.read(4).decode("ascii")
                print(f"Displaying AIFF File Header Data for File {os.path.basename(self.file_path)}")
                print(f"Number of Bytes: {os.path.getsize(self.file_path)}")
                print("Reading AIFF Header...")
                print(f"Chunk Size: {size}")
                print(f"Format: {format_name}")

                while True:
                    chunk_name, chunk_size = struct.unpack(">4sI", file.read(8))
                    if chunk_name == b"COMM":
                        if size <= 18:  # AIFF
                            self.analyze_comm_chunk_aiff(file, chunk_size)
                        else:  # AIFC
                            self.analyze_comm_chunk_aifc(file, chunk_size)
                    elif chunk_name == b"SSND":
                        self.analyze_ssnd_chunk(file, chunk_size)
                    else:
                        file.seek(chunk_size, 1)
        except FileNotFoundError:
            print("Error: File not found.")
        except Exception as e:
            print(f"Error analyzing AIFF file: {e}")

    def analyze_comm_chunk_aiff(self, file, chunk_size):
        num_channels, num_frames, bits_per_sample = struct.unpack(">2Hh", file.read(8))
        print(f"Reading COMM chunk (size: {chunk_size})")
        print(f"Number of Channels: {num_channels}")
        print(f"Number of Frames: {num_frames}")
        print(f"Bits per Sample: {bits_per_sample}")
        sample_rate = struct.unpack(">Q", file.read(8))[0] / 65536
        print(f"Sample Rate: {sample_rate}")

    def analyze_comm_chunk_aifc(self, file, chunk_size):
        num_channels, num_frames, bits_per_sample = struct.unpack(">2Hh", file.read(8))
        print(f"Reading COMM chunk (size: {chunk_size})")
        print(f"Number of Channels: {num_channels}")
        print(f"Number of Frames: {num_frames}")
        print(f"Bits per Sample: {bits_per_sample}")
        sample_rate = struct.unpack(">Q", file.read(8))[0] / 65536
        print(f"Sample Rate: {sample_rate}")
        compression_type = file.read(4).decode("ascii")
        print(f"Compression Type: {compression_type}")
        compression_name = file.read(chunk_size - 22).decode("ascii")
        print(f"Compression Name: {compression_name}")

    def analyze_ssnd_chunk(self, file, chunk_size):
        print(f"Reading SSND chunk (size: {chunk_size})")
        offset, block_size = struct.unpack(">2I", file.read(8))
        print(f"Offset: {offset}")
        print(f"Block Size: {block_size}")

# Example usage:
file_path = input("Enter the path of the AIFF file to analyze: ")
analyzer = AIFFAnalyzer(file_path)
analyzer.analyze_aiff_header()
