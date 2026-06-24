import os

from Form_converter.GraphObj_DotFile_converter import dot_to_Graph
from RandomWalksGenerator import generate_prefixed_closed_negative_walks, \
    generate_prefixed_closed_negative_walks_state_cover, generate_prefixed_closed_negative_walks_transition_cover, \
    generate_pos_test_walks, generate_neg_test_walks
from read_commands import extract_parameters
from retrive_traces import retrieve_traces
from write_clear_file import write_to_file_in_new_line, clear_file


def state_cover_checker(commands_file):
    with open(commands_file, 'r') as file:
        lines = file.readlines()
        for command_string in lines:
            parameters = extract_parameters(command_string)
            # Read Reference graph
            ref_graph = dot_to_Graph(f'reference_automata/{parameters['system']}_reference.dot')
            ref_graph.input_alphabet.sort()
            print(f'{parameters['seed']} {parameters['system']} {parameters['trail']} {parameters['training_size']} {parameters['test_size']}')
            # Generate walks
            training_neg_walks = generate_prefixed_closed_negative_walks(parameters['training_size'], ref_graph, parameters['seed'] * 2)

def generate_state_cover_prefix_closed_traces(commands_file):
    with open(commands_file, 'r') as file:
        lines = file.readlines()
        for command_string in lines:
            parameters = extract_parameters(command_string)
            # Read Reference graph
            ref_graph = dot_to_Graph(f'reference_automata/{parameters['system']}_reference.dot')
            ref_graph.input_alphabet.sort()
            print(f'{parameters['seed']} {parameters['system']} {parameters['trail']} {parameters['training_size']} {parameters['test_size']}')
            # Generate walks
            training_neg_walks = generate_prefixed_closed_negative_walks_state_cover(parameters['training_size'], ref_graph, parameters['seed'])

            output_dir = f"Traces/state_cover_traces/{parameters['system']}"
            os.makedirs(output_dir, exist_ok=True)

            trace_file_name = f'{output_dir}/{parameters['system']}_{parameters['seed']}_{parameters['trail']}_{parameters['training_size']}_state_cover_traces.txt'
            write_to_file_in_new_line(trace_file_name, '__________Learning_Negative Traces_________')
            for walk in training_neg_walks:
                write_to_file_in_new_line(trace_file_name, ','.join(walk))

def generate_transition_cover_prefix_closed_traces(commands_file):
    with open(commands_file, 'r') as file:
        lines = file.readlines()
        for command_string in lines:
            parameters = extract_parameters(command_string)
            # Read Reference graph
            ref_graph = dot_to_Graph(f'reference_automata/{parameters['system']}_reference.dot')
            ref_graph.input_alphabet.sort()
            print(f'{parameters['seed']} {parameters['system']} {parameters['trail']} {parameters['training_size']} {parameters['test_size']}')
            # Generate walks
            training_neg_walks = generate_prefixed_closed_negative_walks_transition_cover(parameters['training_size'], ref_graph, parameters['seed'])

            output_dir = f"Traces/transition_cover_traces/{parameters['system']}"
            os.makedirs(output_dir, exist_ok=True)

            trace_file_name = (f'{output_dir}/'
                               f'{parameters['system']}_{parameters['seed']}_{parameters['trail']}_{parameters['training_size']}_transition_cover_traces.txt')
            clear_file(trace_file_name)
            write_to_file_in_new_line(trace_file_name, '__________Learning_Negative Traces_________')
            for walk in training_neg_walks:
                write_to_file_in_new_line(trace_file_name, ','.join(walk))
def generate_test_data(folder_path, training_data_fileName):
    parts = training_data_fileName.split('_')
    system = parts[0]
    seed_value= int(parts[1])
    trail = int(parts[2])
    training_size = int(parts[3])
    test_size = int(parts[3])*4
    # ignore_list = [5847, 7440, 8857, 845 , 896, 5216 ,1336, 1409, 105, 7674, 8098, 830, 9875, 1889, 4135, 7399, 1370,
    #                5103, 9825, 8060, 9331, 4315, 6292, 5766, 9635, 189, 6096, 4772, 9743, 9919, 9010, 248, 5209, 8195,
    #                6006]
    # if seed_value in ignore_list and system=='coffeemachine':
    #     return
    # Read Reference graph
    ref_graph = dot_to_Graph(f'reference_automata/{system}_reference.dot')
    ref_graph.input_alphabet.sort()
    print(f'{seed_value} {system} {trail} {training_size} {test_size}')

    # Retrieve training negative walks
    file_path = os.path.join(folder_path, training_data_fileName)
    training_neg_walks = retrieve_traces(file_path)[1]

    # Generate test walks
    test_pos_walks = generate_pos_test_walks(test_size, ref_graph, seed_value)
    write_to_file_in_new_line(file_path,'__________EVALUATION_Positive Traces_________')
    for walk in test_pos_walks:
        write_to_file_in_new_line(file_path, ','.join(walk))

    test_neg_walks = generate_neg_test_walks(ref_graph, seed_value, test_size, training_neg_walks)
    write_to_file_in_new_line(file_path, '__________EVALUATION_Negative Traces_________')
    for walk in test_neg_walks:
        write_to_file_in_new_line(file_path, ','.join(walk))

if __name__ == "__main__":
    commands_file = '../commands_coffeemachine_copy.txt'
    # generate_state_cover_prefix_closed_traces(commands_file)
    generate_transition_cover_prefix_closed_traces(commands_file)
    for system in ['coffeemachine']:#, 'openSSL', 'TCP'
        folder_path = os.path.join('../Traces', 'state_cover_traces', system)
        if not os.path.isdir(folder_path):
            continue
        for file_name in os.listdir(folder_path):
            if file_name.endswith('state_cover_traces.txt'):
                generate_test_data(folder_path, file_name)
