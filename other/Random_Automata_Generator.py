import os

from Basic_objects.Graph import Graph
from Basic_objects.State import State
from Basic_objects.Transition import Transition
import random

from others.otherOther.GraphObj_DotFile_converter import graph_to_dot
from others.otherOther.dot_to_png import dot_to_png

import re


def parse_transitions_to_map(file_path):
    # text_input = """
    # V0 <V0> - L0 -> V6 <V6>
    # V0 <V0> - L1 -> V1 <V1>
    # V1 <V1> - L1 -> V6 <V6>
    # V1 <V1> - L3 -> V2 <V2>
    # """
    """
    Parses transitions and extracts the unique alphabet and state count.
    Returns: { 'map': dict, 'alphabet': list, 'state_count': int }
    """
    """
        Reads a .txt file and extracts the map, alphabet, and state count.
        """
    if not os.path.exists(file_path):
        return f"Error: The file '{file_path}' was not found."

    raw_map = {}
    unique_states = set()
    unique_labels = set()

    # Pattern to capture: Source, Label, Target
    pattern = r"(\w+)\s+<\w+>\s+-\s+(\w+)\s+->\s+(\w+)"

    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                src, label, dest = match.groups()

                # Update sets for metadata
                unique_states.update([src, dest])
                unique_labels.add(label)

                # Build dictionary
                if src not in raw_map:
                    raw_map[src] = {}
                raw_map[src][label] = dest

    return {
        "map": raw_map,
        "alphabet": sorted(list(unique_labels)),
        "state_count": len(unique_states),
        "states": sorted(list(unique_states))
    }



def T(src_key, lbl, dest_key):
    out = random.randint(*OUTPUT_RANGE)
    return Transition(states[src_key], states[dest_key], lbl,  out)

if __name__ == "__main__":
    OUTPUT_RANGE = (1, 3)
    file_path = 'stateChum_random_graph.txt'
    result = parse_transitions_to_map(file_path)
    ALPHABET = result["alphabet"]

    # Initialize States
    states_labels = result["states"]
    states = {label: State(label) for label in states_labels}
    sink_state = State("V_SINK")
    states["V_SINK"] = sink_state

    # Raw data mapping
    raw_map = result["map"]

    graph = {}

    for s_name in states:
        graph[states[s_name]] = {}
        current_transitions = raw_map.get(s_name, {})

        for label in ALPHABET:
            # If transition exists, use it; otherwise, go to SINK
            target_name = current_transitions.get(label, "V_SINK")
            target_state = states[target_name]

            # Structure: graph[source][target] = [TransitionObj]
            if target_state not in graph[states[s_name]]:
                graph[states[s_name]][target_state] = []

            graph[states[s_name]][target_state].append(T(s_name, label, target_name))

    G = Graph()
    G.graph = graph
    G.set_initial_state(states['V0'])
    graph_to_dot(G, '../reference_automata/Random6_reference.dot')
    dot_to_png('../reference_automata/Random6_reference.dot', '../reference_automata/Random6_reference.png')