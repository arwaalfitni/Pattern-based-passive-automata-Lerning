from Basic_objects.Tree import Tree
from Form_converter.GraphObj_DotFile_converter import dot_to_Graph
from Learners.Biased_Sicco_EDSM_Learner import BiasedSicco_Learner
from RandomWalksGenerator import generate_prefixed_closed_negative_walks, generate_pos_test_walks, \
    generate_neg_test_walks
from evaluation import Evaluation


def main():
    seed_value = 8698
    learning_strategy = 'DFASAT'
    systemName = 'coffeemachine'
    trails = 3
    learning_walks_size = 120
    testing_walks_size = learning_walks_size * 4
    file_path = f'{systemName}/NoCover/{learning_strategy}/{systemName}_{trails}_{learning_walks_size}_{learning_strategy}'

    # Read Reference graph
    ref_graph = dot_to_Graph(f'reference_automata/{systemName}_reference.dot')
    ref_graph.input_alphabet.sort()

    # Generate walks
    training_pos_walks = []
    training_neg_walks = generate_prefixed_closed_negative_walks(learning_walks_size, ref_graph, seed_value)
    test_pos_walks = generate_pos_test_walks(testing_walks_size, ref_graph, seed_value)
    test_neg_walks = generate_neg_test_walks(ref_graph, seed_value, testing_walks_size, training_neg_walks)

    graph = dot_to_Graph(f'{file_path}dot')
    apta = Tree()
    apta.G = graph
    edsm = BiasedSicco_Learner(apta)
    # Evaluate the learned graph
    eval = Evaluation(edsm, test_pos_walks, test_neg_walks)
    eval.evaluate_2()
    eval.write_evaluation_report(f'{file_path}_statistic.txt')


if __name__ == '__main__':
    main()