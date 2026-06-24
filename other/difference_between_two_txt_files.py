import difflib
import sys


def compare_files(file1_path, file2_path):
    try:
        with open(file1_path, 'r', encoding='utf-8') as f1, \
                open(file2_path, 'r', encoding='utf-8') as f2:

            file1_lines = f1.readlines()
            file2_lines = f2.readlines()

        # 1. Quick check for identity
        if file1_lines == file2_lines:
            print("--- Result: The files are IDENTICAL. ---")
            return

        # 2. If not identical, find differences
        print("--- Result: The files are DIFFERENT. Comparing now... ---\n")

        # Differ() creates a human-readable delta
        diff = difflib.Differ()
        comparison = list(diff.compare(file1_lines, file2_lines))

        for line in comparison:
            # difflib prefixes:
            # '- ' = line exists in file 1 but not file 2
            # '+ ' = line exists in file 2 but not file 1
            # '? ' = incremental difference within the line
            # '  ' = line is identical in both
            if line.startswith(('-', '+', '?')):
                print(line.rstrip())

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

import hashlib

def get_file_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in chunks to save memory
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def fast_compare(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as f1, \
            open(file2_path, 'r', encoding='utf-8') as f2:

        for line_num, (line1, line2) in enumerate(zip(f1, f2), 1):
            if line1 != line2:
                print(f"Difference found at line {line_num}:")
                print(f"File 1: {line1.strip()}")
                print(f"File 2: {line2.strip()}")
                return  # Remove return if you want to see ALL differences

        # Check if one file is longer than the other
        f1_rem = f1.readline()
        f2_rem = f2.readline()
        if f1_rem or f2_rem:
            print("Files match up to a point, but one file is longer than the other.")

# Usage
if __name__ == "__main__":
    # Replace these with your actual file names
    # compare_files(, )
    if get_file_hash('../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_0_formula.txt') == get_file_hash(
                     '../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_1_formula.txt'):
        print("Files are 100% identical.")
    else:
        fast_compare('../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_0_formula.txt',
                     '../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_1_formula.txt')
    if get_file_hash(
            '../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_0_dfasat_variables.txt') == get_file_hash(
            '../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_1_dfasat_variables.txt'):
        print("Files are 100% identical.")
    else:
        fast_compare('../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_0_dfasat_variables.txt',
                     '../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_1_dfasat_variables.txt')
    if get_file_hash(
            '../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_0_SAT_result.txt') == get_file_hash(
            '../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_1_SAT_result.txt'):
        print("Files are 100% identical.")
    else:
        fast_compare('../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_0_SAT_result.txt.txt',
                     '../openSSL/TransitionCover/BiasedSAT1/openSSL_8_300_BiasedSAT1_1_SAT_result.txt')