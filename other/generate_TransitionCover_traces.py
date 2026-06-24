# Generate walks
import os
import random
import re
import sys

from Form_converter.GraphObj_DotFile_converter import dot_to_Graph
from RandomWalksGenerator import generate_pos_test_walks, \
    generate_neg_test_walks, generate_prefixed_closed_negative_walks_transition_cover_minimal
from write_clear_file import clear_file, write_to_file_in_new_line
def generate_transitioncover_traces(system):
    commands_file1 = f'commands_{system}_transitioncover.txt'
    commands_file2 = f'commands_{system}_transitioncover_sicco.txt'
    ref_graph = dot_to_Graph(f'../reference_automata/{system}_reference.dot')
    ref_graph.input_alphabet.sort()

    output_dir = f"../Traces/transition_cover_traces/{system}"
    os.makedirs(output_dir, exist_ok=True)
    if system in ['coffeemachine', 'TextEditor', 'Random1', 'Random2']:
        training_size_list = [10, 15, 20, 30, 40, 50, 60, 80, 100, 120]
    else:
        training_size_list = [100, 120, 150, 170, 200, 220, 250, 270, 300, 350]

    for training_size in training_size_list:
        for trail in range(10):
            seed = random.randint(1, 10000)
            # Generate walks
            training_neg_walks = generate_prefixed_closed_negative_walks_transition_cover_minimal(training_size, ref_graph, seed)

            trace_file_name = (f'{output_dir}/'
                               f'{system}_{seed}_{trail}_{training_size}_transition_cover_traces.txt')
            clear_file(trace_file_name)
            write_to_file_in_new_line(trace_file_name, '__________Learning_Negative Traces_________')
            for walk in training_neg_walks:
                write_to_file_in_new_line(trace_file_name, ', '.join(walk))


            # Generate test walks
            test_size = training_size * 4
            test_pos_walks = generate_pos_test_walks(test_size, ref_graph, seed)
            write_to_file_in_new_line(trace_file_name, '__________EVALUATION_Positive Traces_________')
            for walk in test_pos_walks:
                write_to_file_in_new_line(trace_file_name, ', '.join(walk))

            test_neg_walks = generate_neg_test_walks(ref_graph, seed, test_size, training_neg_walks)
            write_to_file_in_new_line(trace_file_name, '__________EVALUATION_Negative Traces_________')
            for walk in test_neg_walks:
                write_to_file_in_new_line(trace_file_name, ', '.join(walk))

            write_to_file_in_new_line(commands_file1, f'python3 Run_Learner_transition_cover.py {seed} classicalEDSM {system} {trail} {training_size}')
            write_to_file_in_new_line(commands_file1, f'python3 Run_Learner_transition_cover.py {seed} BiasedEDSM {system} {trail} {training_size}')
            write_to_file_in_new_line(commands_file1, f'python3 Run_Learner_transition_cover.py {seed} BiasedSAT {system} {trail} {training_size}')
            write_to_file_in_new_line(commands_file1, f'python3 Run_Learner_transition_cover.py {seed} BiasedSATPAT {system} {trail} {training_size}')
            write_to_file_in_new_line(commands_file2, f'python3 Run_Learner_transition_cover.py {seed} BiasedSiccoSAT {system} {trail} {training_size}')
            write_to_file_in_new_line(commands_file2,f'python3 Run_Learner_transition_cover.py {seed} BiasedSiccoSATPAT {system} {trail} {training_size}')
            write_to_file_in_new_line(commands_file2,f'python3 Run_Learner_transition_cover.py {seed} DFASAT {system} {trail} {training_size}')

def generate_transitioncover_traces_from_commands(system, commands_file):
    ref_graph = dot_to_Graph(f'../reference_automata/{system}_reference.dot')
    ref_graph.input_alphabet.sort()

    output_dir = f"../Traces/transition_cover_traces/{system}"
    os.makedirs(output_dir, exist_ok=True)
    pat = re.compile(r'^\s*\d+\s*:\s*')
    with open (commands_file, 'r') as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            s = pat.sub("", s)  # remove leading "N :"
            parts = s.split()
            if len(parts) < 4:
                continue
            seed = parts[2]  # third token after header removal
            trail = parts[5]  # second to last
            training_size = int(parts[6])  # last
            # Generate walks
            training_neg_walks = generate_prefixed_closed_negative_walks_transition_cover_minimal(training_size, ref_graph, seed)

            trace_file_name = (f'{output_dir}/'
                               f'{system}_{seed}_{trail}_{training_size}_transition_cover_traces.txt')
            clear_file(trace_file_name)
            write_to_file_in_new_line(trace_file_name, '__________Learning_Negative Traces_________')
            for walk in training_neg_walks:
                write_to_file_in_new_line(trace_file_name, ', '.join(walk))


            # Generate test walks
            test_size = training_size * 4
            test_pos_walks = generate_pos_test_walks(test_size, ref_graph, seed)
            write_to_file_in_new_line(trace_file_name, '__________EVALUATION_Positive Traces_________')
            for walk in test_pos_walks:
                write_to_file_in_new_line(trace_file_name, ', '.join(walk))

            test_neg_walks = generate_neg_test_walks(ref_graph, seed, test_size, training_neg_walks)
            write_to_file_in_new_line(trace_file_name, '__________EVALUATION_Negative Traces_________')
            for walk in test_neg_walks:
                write_to_file_in_new_line(trace_file_name, ', '.join(walk))

def generate_transitioncover_traces_minimum(system):
    ref_graph = dot_to_Graph(f'../reference_automata/{system}_reference.dot')
    ref_graph.input_alphabet.sort()

    output_dir = f"../Traces/transition_cover_minimum_shortTraces/{system}"
    os.makedirs(output_dir, exist_ok=True)
    pat = re.compile(r'^\s*\d+\s*:\s*')

    # Generate walks
    training_neg_walks = generate_prefixed_closed_negative_walks_transition_cover_minimal(0, ref_graph, 0)

    trace_file_name = (f'{output_dir}/'
                       f'{system}_transition_cover_minimum_Traces_Qx2.txt')
    clear_file(trace_file_name)
    write_to_file_in_new_line(trace_file_name, '__________Learning_Negative Traces_________')
    for walk in training_neg_walks:
        write_to_file_in_new_line(trace_file_name, ', '.join(walk))


if __name__ == "__main__":
    system_list = ['TextEditorPaper']#'Random1','coffeemachine', 'bluetooth','TCP', 'openSSL'] #
    for system in system_list:
        # generate_transitioncover_traces(system)
        # generate_transitioncover_traces_from_commands(system, '../commands_Random1_TransitionCover_sicco.txt')
        generate_transitioncover_traces_minimum(system)