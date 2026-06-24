from Form_converter.GraphObj_DotFile_converter import graph_to_dot, dot_to_Graph


def deterministic(state, graph):
    transitions = graph .get_outgoing_transitions_for_state(state)
    seen_inputs = []
    for t in transitions:
        input_symbol = t.input_key
        if t.to_state.type == 'accepted':
            if input_symbol in seen_inputs:
                return False
            else:
                seen_inputs.append(input_symbol)
    return True

def clean_automata_after_EDSM(graph):
    for state in graph.get_all_states():
        if deterministic(state, graph):
            accepted_transitions = [tr for tr in graph.get_outgoing_transitions_for_state(state)if tr.to_state.type == 'accepted']
            transitions = graph.get_outgoing_transitions_for_state(state)
            for t in accepted_transitions:
                for t2 in transitions:
                    if t.input_key == t2.input_key and t != t2 and t2.to_state.type == 'rejected':
                        graph.delete_Transition(t2)
    return graph

#use example:
original_graph = dot_to_Graph(f'../TextEditor/LongTraces/DFASAT/TextEditor_2_15_DFASATEDSM.dot')
cleaned_graph = clean_automata_after_EDSM(original_graph)
graph_to_dot(cleaned_graph, '../TextEditor/LongTraces/DFASAT/TextEditor_2_15_DFASATEDSM_Cleaned.dot')
