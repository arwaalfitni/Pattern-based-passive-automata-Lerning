"""
This script is the main entry point for running the learning experiments. 
It takes command-line arguments to specify the seed value, learning strategy, input file name, number of trails, number of negative walks for inferring the model, and data coverage type.

The script performs the following steps:
1. Parses command-line arguments.
2. Reads the reference graph from a DOT file.
3. Generates training and testing walks based on the specified coverage type.
4. Builds an APTA (Augmented Prefix Tree Acceptor) from the training walks.
5. Depending on the specified learning strategy, it runs the appropriate learning algorithm (e.g., classical EDSM, Biased EDSM, SAT-based learning).
6. Evaluates the learned graph against the test walks and writes the evaluation report to a statistics file.

Run example:
uv run run.py 1185 DFASAT TextEditor 0 5 TransitionCover

"""

import argparse
import os

import time

from Form_converter.GraphObj_DotFile_converter import dot_to_Graph, graph_to_dot
from Learners.Baised_Learner_check_without_merge_1notfollow1 import Baised_Learner1
# from Learners.Baised_Learner_check_without_Merge_2notfollowing1 import Baised_Learner2
from Learners.Biased_Sicco_EDSM_Learner import BiasedSicco_Learner
from Learners.Classical_Learner import Learner
from Learners.DFASAT.SAT import SAT
from Learners.Sicco_Learner import Sicco_Learner
from Patterns.pattern_from_traces.Explore_PTA import save_Exploration_map_to_file
from Basic_objects.Tree import Tree
from RandomWalksGenerator import generate_prefixed_closed_negative_walks, \
    generate_pos_test_walks, generate_neg_test_walks, add_more_random_prefixed_closed_traces, \
    generate_pos_test_walks_short_length, generate_neg_test_walks_short_length
from evaluation import Evaluation
from retrive_traces import retrieve_traces
from write_clear_file import write_to_file_in_new_line, clear_file


def main():
    parser = argparse.ArgumentParser(description="Process seed, file name, and trail count.")
    parser.add_argument("seed", type=int, help="Integer seed value")
    parser.add_argument("learning_strategy", type=str, help="approach of learning")
    parser.add_argument("filename", type=str, help="Input file name")
    parser.add_argument("trails", type=int, help="Number of trails")
    parser.add_argument("learning_walks_size", type=int, help="Number of negative walks for inferring the model")
    parser.add_argument("coverage", type=str, help="Data Coverage type")

    args = parser.parse_args()

    seed_value = args.seed
    learning_strategy = args.learning_strategy
    systemName = args.filename
    trails = args.trails
    learning_walks_size = args.learning_walks_size
    # testing_walks_size = learning_walks_size*4
    coverage = args.coverage

    file_path = f'{systemName}/{coverage}/{learning_strategy}/{systemName}_{trails}_{learning_walks_size}_{learning_strategy}'
    statistic_file_path = f'outputs/{file_path}_statistics.txt'


    # Create directories if they don't exist
    dir = os.path.dirname(statistic_file_path)
    os.makedirs(dir, exist_ok=True)

    # Read Reference graph
    ref_graph = dot_to_Graph(f'reference_automata/{systemName}_reference.dot')
    ref_graph.input_alphabet.sort()
    clear_file(statistic_file_path)
    write_to_file_in_new_line(statistic_file_path,
                              f'File: {systemName}\n'
                              f'Seed: {seed_value}\n'
                              f'Trails: {trails}\n'
                              f'Number of walks: {learning_walks_size}\n'
                              f'Size of reference graph: {len(ref_graph.get_all_states())} states\n'
                              f'Alphabet_size: {len(ref_graph.alphabet)} symbols\n')
    training_pos_walks=[]; training_neg_walks = []; test_pos_walks =[]; test_neg_walks =[]
    # Generate walks
    if coverage == 'NoCover':
        training_neg_walks = generate_prefixed_closed_negative_walks(learning_walks_size, ref_graph, seed_value)
        testing_walks_size = len(training_neg_walks) * 4
        test_pos_walks = generate_pos_test_walks(testing_walks_size, ref_graph, seed_value)
        test_neg_walks = generate_neg_test_walks(ref_graph, seed_value, testing_walks_size, training_neg_walks)
    elif coverage == 'StateCover':
        _, minimum_neg_walks, _p, _n = retrieve_traces(
            f'Traces/state_cover_minimum_shortTraces/{systemName}/{systemName}_state_cover_minimum_shortTraces.txt')
        training_neg_walks = add_more_random_prefixed_closed_traces(minimum_neg_walks, learning_walks_size, seed_value, ref_graph)
        testing_walks_size = len(training_neg_walks) * 4
        test_pos_walks = generate_pos_test_walks(testing_walks_size, ref_graph, seed_value)
        test_neg_walks = generate_neg_test_walks(ref_graph, seed_value, testing_walks_size, training_neg_walks)
    elif coverage == 'TransitionCover':
        _, minimum_neg_walks, _p, _n = retrieve_traces(
            f'Traces/transition_cover_minimum_shortTraces/{systemName}/{systemName}_transition_cover_minimum_shortTraces.txt')
        training_neg_walks = add_more_random_prefixed_closed_traces(minimum_neg_walks, learning_walks_size, seed_value, ref_graph)
        testing_walks_size = len(training_neg_walks) * 4
        test_pos_walks = generate_pos_test_walks_short_length(testing_walks_size, ref_graph, seed_value)
        test_neg_walks = generate_neg_test_walks_short_length(ref_graph, seed_value, testing_walks_size, training_neg_walks)

    # Build APTA
    apta = Tree()
    apta.build_labeled_tree(ref_graph, training_pos_walks, training_neg_walks)

    # Delete all Rejected states
    apta.G.delete_rejected_states()

    write_to_file_in_new_line('outputs/raw-data.txt',f'System Name:{systemName}\nNumber of Traces:{len(training_neg_walks)}\nNumber of states: {len(apta.G.get_all_states())}\nNumber of edges: {len(apta.G.get_all_transitions())}')
    # RUN classical EDSM
    # total_edsm_time = 0.0
    # start_time = time.time()
    # edsm = None
    # if learning_strategy == 'SATafterBiasedEDSM':
    #     graph = dot_to_Graph(
    #         f'{systemName}/{coverage}/{learning_strategy}/{systemName}_{trails}_{learning_walks_size}_BiasedEDSM1.dot')
    #     apta = Tree()
    #     edsm = Baised_Learner1(apta)
    #     edsm.pta.G = graph
    #     edsm.setup(f'{file_path}_mergeTracker.txt')
    # if learning_strategy == 'classicalEDSM':
    #     edsm = Learner(apta)
    #     edsm.setup(f'mergeTracker.txt')
    #     edsm.run_EDSM_learner()
    # elif learning_strategy in ['BiasedEDSM1', 'BiasedSAT1', 'BiasedSATPAT1']:
    #     edsm = Baised_Learner1(apta)
    #     edsm.setup(f'{file_path}_mergeTracker.txt')
    #     save_Exploration_map_to_file(edsm.hard_patterns,f'{file_path}_hard_map.txt')
    #     if learning_strategy == 'BiasedEDSM1':
    #         edsm.run_EDSM_with_pattern_learner()
    #     elif learning_strategy in ['BiasedSATPAT1', 'BiasedSAT1']:
    #         graph_to_dot(edsm.pta.G, f'{file_path}_pta.dot')
    #         edsm.run_EDSM_with_pattern_learner_partial_merger()
    # elif learning_strategy in ['BiasedEDSM2', 'BiasedSAT2', 'BiasedSATPAT2']:
    #     edsm = Baised_Learner2(apta)
    #     edsm.setup(f'{file_path}_mergeTracker.txt')
    #     save_Exploration_map_to_file(edsm.hard_patterns,f'{file_path}_hard_map.txt')
    #     if learning_strategy == 'BiasedEDSM2':
    #         edsm.run_EDSM_with_pattern_learner()
    #     elif learning_strategy in ['BiasedSATPAT2', 'BiasedSAT2']:
    #         edsm.run_EDSM_with_pattern_learner_partial_merger()
    # elif learning_strategy in ['BiasedSiccoSAT', 'BiasedSiccoSATPAT']:
    #     edsm = BiasedSicco_Learner(apta)
    #     edsm.setup(f'mergeTracker.txt')
    #     save_Exploration_map_to_file(edsm.hard_patterns,f'{file_path}_hard_map.txt')
    #     edsm.run_SiccoEDSM_with_pattern_learner_partial_merger()
    # elif learning_strategy == 'DFASAT':
    #     edsm = Sicco_Learner(apta)
    #     edsm.setup(f'{file_path}_mergeTracker.txt')
    #     edsm.run_Sicco_learner()
    #
    # total_edsm_time += time.time() - start_time
    # edsm.write_statistics(statistic_file_path)
    # write_to_file_in_new_line(statistic_file_path,
    #                           f'Total time spent in EDSM (seconds): {total_edsm_time:.4f}\n')
    #
    #
    # if learning_strategy in ['BiasedSAT1', 'BiasedSAT2', 'BiasedSATPAT1', 'BiasedSATPAT2','BiasedSiccoSAT', 'BiasedSiccoSATPAT', 'DFASAT','SATafterBiasedEDSM']:
    #     graph_to_dot(edsm.pta.G, f'{file_path}EDSM.dot')
    #     # Run SAT
    #     total_sat_time = 0.0
    #     start_time = time.time()
    #     color_limit = int(len(ref_graph.get_all_states())*2)
    #     sat_solver = SAT(edsm.pta.G, color_limit)
    #     if learning_strategy in ['BiasedSAT1', 'BiasedSAT2','BiasedSiccoSAT', 'DFASAT','SATafterBiasedEDSM']:
    #         dfasat_graph = sat_solver.run_dfasat(file_path)
    #     else:
    #          dfasat_graph = sat_solver.run_dfasat_with_patterns(file_path, edsm.hard_patterns)
    #     total_sat_time += time.time() - start_time
    #     sat_solver.write_dfasat_report(statistic_file_path)
    #     write_to_file_in_new_line(statistic_file_path,
    #                               f'Total time spent in SAT solver (seconds): {total_sat_time:.4f}\n')
    #
    #     # Delete formula file to save disk space
    #     formula_file = f'{file_path}_formula.txt'
    #     if os.path.exists(formula_file):
    #         os.remove(formula_file)
    #
    #     if dfasat_graph:
    #         graph_to_dot(dfasat_graph, f'{file_path}.dot')
    #         edsm.pta.G = dfasat_graph
    #         # Evaluate the learned graph
    #         eval = Evaluation(edsm, test_pos_walks, test_neg_walks)
    #         eval.evaluate_2()
    #         eval.write_evaluation_report(statistic_file_path)
    #
    # else:
    #     graph_to_dot(edsm.pta.G,f'{file_path}.dot')
    #     # Evaluate the learned graph
    #     eval = Evaluation(edsm, test_pos_walks, test_neg_walks)
    #     eval.evaluate_2()
    #     eval.write_evaluation_report(statistic_file_path)

if __name__ == '__main__':
    main()