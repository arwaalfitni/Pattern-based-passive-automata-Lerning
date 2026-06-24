import argparse
import os

import time

from Form_converter.GraphObj_DotFile_converter import dot_to_Graph, graph_to_dot
from Learners.Baised_Learner import Baised_Learner
from Learners.Biased_Sicco_EDSM_Learner import BiasedSicco_Learner
from Learners.Classical_Learner import Learner
from Learners.DFASAT.SAT import SAT
from Learners.Sicco_Learner import Sicco_Learner
from Patterns.pattern_from_traces.Explore_PTA import save_Exploration_map_to_file, explor_whatis_whatisnot_next, \
    hard_vs_soft_patterns
from Basic_objects.Tree import Tree
from RandomWalksGenerator import generate_prefixed_closed_negative_walks, generate_pos_test_walks, \
    generate_neg_test_walks
# from RandomWalksGenerator import generate_prefixed_closed_negative_walks, \
#     split_into_evaluation_and_training_lists, generate_pos_test_walks, generate_neg_test_walks
from evaluation import Evaluation
from retrive_traces import retrieve_traces
from write_clear_file import write_to_file_in_new_line, clear_file


def main():
    parser = argparse.ArgumentParser(description="Process seed, file name, and trail count.")
    parser.add_argument("coverage", type=str, help="coverage")
    parser.add_argument("seed", type=int, help="Integer seed value")
    parser.add_argument("learning_strategy", type=str, help="approach of learning")
    parser.add_argument("filename", type=str, help="Input file name")
    parser.add_argument("trails", type=int, help="Number of trails")
    parser.add_argument("learning_walks_size", type=int, help="Number of negative walks for inferring the model")
    # parser.add_argument("testing_walks_size", type=int, help="Number of positive and negative walks for testing the inferred model")

    args = parser.parse_args()
    coverage = args.coverage
    seed_value = args.seed
    learning_strategy = args.learning_strategy
    systemName = args.filename
    trails = args.trails
    learning_walks_size = args.learning_walks_size
    testing_walks_size = learning_walks_size*4
    # Read Reference graph
    ref_graph = dot_to_Graph(f'reference_automata/{systemName}_reference.dot')
    ref_graph.input_alphabet.sort()

    file_path = ''
    training_pos_walks = []
    training_neg_walks = []
    test_pos_walks = []
    test_neg_walks = []

    if coverage == 'NoCover':
        file_path = f'{systemName}/NoCover/{learning_strategy}/{systemName}_{trails}_{learning_walks_size}_{learning_strategy}'

        # Create directories if they don't exist
        os.makedirs(f'{systemName}', exist_ok=True)
        os.makedirs(f'{systemName}/NoCover', exist_ok=True)
        os.makedirs(f'{systemName}/NoCover/{learning_strategy}', exist_ok=True)

        # Generate walks
        training_pos_walks = []
        training_neg_walks = generate_prefixed_closed_negative_walks(learning_walks_size, ref_graph, seed_value)
        test_pos_walks = generate_pos_test_walks(testing_walks_size, ref_graph, seed_value)
        test_neg_walks = generate_neg_test_walks(ref_graph, seed_value, testing_walks_size, training_neg_walks)
    # elif coverage == 'StateCover':
    #     file_path = f'{systemName}/StateCover/{learning_strategy}/{systemName}_{trails}_{learning_walks_size}_{learning_strategy}'
    #
    #     # Create directories if they don't exist
    #     os.makedirs(f'{systemName}', exist_ok=True)
    #     os.makedirs(f'{systemName}/StateCover', exist_ok=True)
    #     os.makedirs(f'{systemName}/StateCover/{learning_strategy}', exist_ok=True)
    #     # Generate walks
    #     training_pos_walks = []
    #     _, training_neg_walks, test_pos_walks, test_neg_walks = retrieve_traces(
    #         f'Traces/state_cover_traces/{systemName}/{systemName}_{seed_value}_{trails}_{learning_walks_size}_state_cover_traces.txt')


    # Build APTA
    apta = Tree()
    apta.build_labeled_tree(ref_graph, training_pos_walks, training_neg_walks)
    exploration_map = explor_whatis_whatisnot_next(apta)
    hard_patterns, soft_patterns = hard_vs_soft_patterns(exploration_map)
    save_Exploration_map_to_file(hard_patterns,f'{file_path}_hard_map.txt')
    save_Exploration_map_to_file(soft_patterns,f'{file_path}_soft_map.txt')


if __name__ == '__main__':
    main()