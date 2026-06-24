def delete_lines(input_file, output_file):
    """
    Deletes specified lines from a text file.

    :param input_file: Path to the input text file.
    :param output_file: Path to the output text file where the result will be saved.
    :param lines_to_delete: A set of line numbers (1-indexed) to delete from the file.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for lineno, line in enumerate(infile, start=1):
                    if 'classicalEDSM' in line:
                        outfile.write(line)



if __name__ == "__main__":
    input_file = '../commands_TCP.txt'
    output_file = '../commands_TCP_copy.txt'
    delete_lines(input_file, output_file)