import os
import subprocess

def decompress_if_needed(input_path):
    """
    Checks if the input file is compressed (.zst) and decompresses it if needed.
    Returns the path to the decompressed file.
    """
    if input_path.endswith('.zst'):
        # Remove exactly 4 characters (".zst") from the end
        decompressed_path = input_path[:-4]
        if not os.path.exists(decompressed_path):
            print(f"Decompressing {input_path} to {decompressed_path} ...")
            subprocess.run(["unzstd", input_path], check=True)
        return decompressed_path
    return input_path
