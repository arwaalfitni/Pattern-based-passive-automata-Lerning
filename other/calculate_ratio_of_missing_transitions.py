import os

from Form_converter.GraphObj_DotFile_converter import dot_to_Graph
from write_clear_file import write_to_file_in_new_line


def calculate_ratio_of_missing_transitions(doFile, system, statistic_file_path):
    learnt_graph = dot_to_Graph(doFile)
    transitions_in_learnt = len(learnt_graph.get_all_transitions())
    reference_graph = dot_to_Graph(f'../reference_automata/{system}_reference.dot')
    actual_transitions_in_reference = len(reference_graph.get_all_transitions())
    ratio = round( 1.0 - (transitions_in_learnt/actual_transitions_in_reference), 2)
    write_to_file_in_new_line(statistic_file_path, f'Ratio of Missing Transitons: {ratio}')


if __name__ == '__main__':
    system = 'bluetooth'
    #trace_size = [0, 1, 3, 6, 12, 25, 50]
    # trace_size = [0, 4, 9, 18, 37, 75, 150]
    trace_size = [300, 600, 1200]
    main_folder = f'/home/arwaalfitni/pycharmProjects/HPCExperimentResult/PositiveOnly_minimumCoverage_shortTraces/{system}/TransitionCover_moreTraces/BiasedEDSM1/'
    for trail in range(9):
        for size in trace_size:
            statistics_file=None; graph_file=None
            for file in os.listdir(main_folder):
                if file.endswith(f'_{trail}_{size}_BiasedEDSM1_statistics.txt'):
                    statistics_file = os.path.join(main_folder, file)
                elif file.endswith(f'_{trail}_{size}_BiasedEDSM1.dot'):
                    graph_file = os.path.join(main_folder, file)
            if statistics_file and graph_file:
                calculate_ratio_of_missing_transitions(graph_file, system, statistics_file)

        # graph_file='../coffeemachine/TransitionCover/BiasedEDSM1/coffeemachine_0_0_BiasedEDSM1.dot'
        # statistics_file = '../coffeemachine/TransitionCover/BiasedEDSM1/coffeemachine_0_0_BiasedEDSM1_statistics.txt'