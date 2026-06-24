import random

def generate_positive_walks_NoCover(positive_walks_size, graph, seed_value):
    rng = random.Random(seed_value)
    # positive walks that are not neccessarily cover all transitions and states
    positive_walks = []
    visited_states = [graph.initial_state]
    graph_size = len(graph.get_all_states())
    while len(positive_walks) < positive_walks_size :
        walk = []
        current_state = graph.initial_state
        _continue = True
        while _continue or len(walk) < (graph_size*2):
            input_key = f'{rng.choice(graph.input_alphabet)}'
            output_key = graph.get_output(current_state, input_key)
            walk.append(f'{input_key}/{output_key}')
            current_state = graph.get_target_state(current_state, input_key)
            if current_state not in visited_states:
                visited_states.append(current_state)
            _continue = rng.uniform(0, 1) >= 0.5
        if walk not in positive_walks:
            positive_walks.append(walk)
    if len(visited_states) < graph_size:
         print(
                f'Warning: generated positive walks did not visit all states. visited states: {len(visited_states)}, graph size: {graph_size}')
    return positive_walks

def generate_positive_walks_state_cover_minimal(
    positive_walks_size, graph, seed_value, epsilon=0.2
):
    """
    Generate negative walks using two phases:
      1. Guided random walk (ε-greedy) until transition coverage is achieved.
      2. Pure random walks until negative_walks_size is reached.
    Each generated walk is a valid continuous path (no teleportation).
    """

    rng = random.Random(seed_value)
    positive_walks = []
    visited_states = [graph.initial_state]
    visited_transitions = set()

    graph_size = len(graph.get_all_states())
    transition_size = len(graph.get_all_transitions())
    state_cover = False

    # ============================================================
    # 🩵 Phase 1: Guided Random Walk — reach transition coverage
    # ============================================================
    # print("Phase 1: Guided random walk until transition coverage...")

    while not state_cover:
        walk = []
        current_state = graph.initial_state
        _continue = True

        add_new_state = False

        while _continue or len(walk) < (graph_size * 2):
            children = graph.get_children(current_state)
            uncovered = [s for s in children if s not in visited_states]

            # ---- Input selection ----
            if uncovered and rng.random() > epsilon:
                # Exploit uncovered transitions
                next_state = rng.choice(uncovered)
            else:
                # Explore randomly
                next_state = rng.choice(children)

            # ---- Execute transition ----
            trnsitions_between_states = graph.graph[current_state][next_state]
            current_transition = rng.choice(trnsitions_between_states)
            walk.append(f"{current_transition.input_key}/{current_transition.output_key}")

            visited_transitions.add(current_transition)
            if next_state not in visited_states:
                visited_states.append(next_state)
                add_new_state = True
            current_state = next_state

            # Continue randomly
            _continue = rng.uniform(0, 1) >= 0.5

            # Check for completion
            if len(visited_states) == graph_size:
                state_cover = True
                print(f"✅ State coverage reached ({graph_size} transitions).")
                break

        # ---- Add final negative transition ----
        input_key = rng.choice(graph.input_alphabet)
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f"{input_key}/{output_key}")

        if walk not in positive_walks and add_new_state:
            positive_walks.append(walk)

    # ============================================================
    # 🩶 Phase 2: Pure Random Walks — fill until walk count reached
    # ============================================================
    # print("Phase 2: Pure random walks until walk limit reached...")

    while len(positive_walks) < positive_walks_size:
        walk = []
        current_state = graph.initial_state
        _continue = True

        while _continue or len(walk) < (graph_size * 2):
            input_key = rng.choice(graph.input_alphabet)
            output_key = graph.get_output(current_state, input_key)
            walk.append(f"{input_key}/{output_key}")
            current_state = graph.get_target_state(current_state, input_key)
            _continue = rng.uniform(0, 1) >= 0.5

        # ---- Add final negative transition ----
        input_key = rng.choice(graph.input_alphabet)
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f"{input_key}/{output_key}")

        if walk not in positive_walks:
            positive_walks.append(walk)

    # ============================================================
    # 🧾 Diagnostics
    # ============================================================
    if len(visited_states) < graph_size:
        print(
            f"Warning: generated walks did not visit all states "
            f"({len(visited_states)} of {graph_size})."
        )
    if len(visited_transitions) < transition_size:
        print(
            f"Warning: not all transitions were covered "
            f"({len(visited_transitions)} of {transition_size})."
        )

    return positive_walks


def generate_positive_transition_cover_minimal(
    positive_walks_size, graph, seed_value, epsilon=0.2
):
    """
    Generate negative walks using two phases:
      1. Guided random walk (ε-greedy) until transition coverage is achieved.
      2. Pure random walks until negative_walks_size is reached.
    Each generated walk is a valid continuous path (no teleportation).
    """

    rng = random.Random(seed_value)
    positive_walks = []
    visited_states = [graph.initial_state]
    visited_transitions = set()

    graph_size = len(graph.get_all_states())
    transition_size = len(graph.get_all_transitions())
    transition_cover = False

    # ============================================================
    # 🩵 Phase 1: Guided Random Walk — reach transition coverage
    # ============================================================
    # print("Phase 1: Guided random walk until transition coverage...")

    while not transition_cover:
        walk = []
        current_state = graph.initial_state
        _continue = True

        add_new_transition = False

        while _continue or len(walk) < (graph_size * 2):
            outgoing_transitions = graph.get_outgoing_transitions_for_state(current_state)
            uncovered = [t for t in outgoing_transitions if t not in visited_transitions]

            # ---- Input selection ----
            if uncovered and rng.random() > epsilon:
                # Exploit uncovered transitions
                chosen_transition = rng.choice(uncovered)
                input_key = chosen_transition.input_key
            else:
                # Explore randomly
                input_key = rng.choice(graph.input_alphabet)

            # ---- Execute transition ----
            output_key = graph.get_output(current_state, input_key)
            next_state = graph.get_target_state(current_state, input_key)
            walk.append(f"{input_key}/{output_key}")

            # ---- Update coverage ----
            current_transition = graph.get_outgoing_transitions_for_state_with_input(
                current_state, input_key
            )
            if current_transition not in visited_transitions:
                add_new_transition = True
            visited_transitions.add(current_transition)
            if next_state not in visited_states:
                visited_states.append(next_state)
            current_state = next_state

            # Continue randomly
            _continue = rng.uniform(0, 1) >= 0.5

            # Check for completion
            if len(visited_transitions) == transition_size:
                transition_cover = True
                print(f"✅ Transition coverage reached ({transition_size} transitions).")
                break

        # ---- Add final negative transition ----
        input_key = rng.choice(graph.input_alphabet)
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f"{input_key}/{output_key}")

        if walk not in positive_walks and add_new_transition:
            positive_walks.append(walk)

    # ============================================================
    # 🩶 Phase 2: Pure Random Walks — fill until walk count reached
    # ============================================================
    # print("Phase 2: Pure random walks until walk limit reached...")

    while len(positive_walks) < positive_walks_size:
        walk = []
        current_state = graph.initial_state
        _continue = True

        while _continue or len(walk) < (graph_size * 2):
            input_key = rng.choice(graph.input_alphabet)
            output_key = graph.get_output(current_state, input_key)
            walk.append(f"{input_key}/{output_key}")
            current_state = graph.get_target_state(current_state, input_key)
            _continue = rng.uniform(0, 1) >= 0.5

        # ---- Add final negative transition ----
        input_key = rng.choice(graph.input_alphabet)
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f"{input_key}/{output_key}")

        if walk not in positive_walks:
            positive_walks.append(walk)

    # ============================================================
    # 🧾 Diagnostics
    # ============================================================
    if len(visited_states) < graph_size:
        print(
            f"Warning: generated walks did not visit all states "
            f"({len(visited_states)} of {graph_size})."
        )
    if len(visited_transitions) < transition_size:
        print(
            f"Warning: not all transitions were covered "
            f"({len(visited_transitions)} of {transition_size})."
        )

    return positive_walks


def generate_prefixed_closed_negative_walks(negative_walks_size, graph, seed_value):
    rng = random.Random(seed_value)
    negative_walks = []
    visited_states = [graph.initial_state]
    graph_size = len(graph.get_all_states())
    while len(negative_walks) < negative_walks_size:
        walk = []
        current_state = graph.initial_state
        _continue = True
        while _continue or len(walk) < (graph_size*2):
            input_key = f'{rng.choice(graph.input_alphabet)}'
            output_key = graph.get_output(current_state, input_key)
            walk.append(f'{input_key}/{output_key}')
            current_state = graph.get_target_state(current_state, input_key)
            if current_state not in visited_states:
                visited_states.append(current_state)
            _continue = rng.uniform(0, 1) >= 0.5
        # generate the last transition that makes the walk negative. (add not exsitiing transition to the walk)
        input_key = f'{rng.choice(graph.input_alphabet)}'
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f'{input_key}/{output_key}')

        if walk not in negative_walks:
            negative_walks.append(walk)
    if len(visited_states) < graph_size:
        print(f'Warning: generated negative walks did not visit all states. visited states: {len(visited_states)}, graph size: {graph_size}')
    return negative_walks


#def generate_prefixed_closed_negative_walks_state_cover(negative_walks_size, graph, seed_value):
    rng = random.Random(seed_value)
    negative_walks = []
    visited_states = [graph.initial_state]
    state_cover = False
    visited_transitions = []
    graph_size = len(graph.get_all_states())
    while len(negative_walks) < negative_walks_size or not state_cover:
        walk = []
        current_state = graph.initial_state
        _continue = True
        while _continue or len(walk) < (graph_size*2):
            input_key = f'{rng.choice(graph.input_alphabet)}'
            output_key = graph.get_output(current_state, input_key)
            walk.append(f'{input_key}/{output_key}')
            current_state = graph.get_target_state(current_state, input_key)
            if current_state not in visited_states:
                visited_states.append(current_state)
            _continue = rng.uniform(0, 1) >= 0.5
            if len(visited_states) == graph_size:
                state_cover = True
            current_transition = graph.get_outgoing_transitions_for_state_with_input(current_state, input_key)
            if current_transition not in visited_transitions:
                visited_transitions.append(current_transition)
        # generate the last transition that makes the walk negative. (add not exsitiing transition to the walk)
        input_key = f'{rng.choice(graph.input_alphabet)}'
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f'{input_key}/{output_key}')

        if walk not in negative_walks:
            negative_walks.append(walk)
    if len(visited_states) < graph_size:
        print(f'Warning: generated negative walks did not visit all states. visited states: {len(visited_states)}, graph size: {graph_size}')
    transition_size = len(graph.get_all_transitions())
    if len(visited_transitions) < transition_size:
        print(
                f'Warning: generated negative walks did not visit all transitions. '
                f'visited transitions: {len(visited_transitions)}, '
                f'graph transitions size: {transition_size}')
    return negative_walks


# def generate_prefixed_closed_negative_walks_transition_cover(
#     negative_walks_size, graph, seed_value, epsilon=0.2
# ):
#     """
#     Generate negative walks using two phases:
#       1. Guided random walk (ε-greedy) until transition coverage is achieved.
#       2. Pure random walks until negative_walks_size is reached.
#     Each generated walk is a valid continuous path (no teleportation).
#     """
#
#     rng = random.Random(seed_value)
#     negative_walks = []
#     visited_states = [graph.initial_state]
#     visited_transitions = set()
#
#     graph_size = len(graph.get_all_states())
#     transition_size = len(graph.get_all_transitions())
#     transition_cover = False
#
#     # ============================================================
#     # 🩵 Phase 1: Guided Random Walk — reach transition coverage
#     # ============================================================
#     # print("Phase 1: Guided random walk until transition coverage...")
#
#     while not transition_cover:
#         walk = []
#         current_state = graph.initial_state
#         _continue = True
#
#         while _continue or len(walk) < (graph_size * 2):
#             outgoing_transitions = graph.get_outgoing_transitions_for_state(current_state)
#             uncovered = [t for t in outgoing_transitions if t not in visited_transitions]
#
#             # ---- Input selection ----
#             if uncovered and rng.random() > epsilon:
#                 # Exploit uncovered transitions
#                 chosen_transition = rng.choice(uncovered)
#                 input_key = chosen_transition.input_key
#             else:
#                 # Explore randomly
#                 input_key = rng.choice(graph.input_alphabet)
#
#             # ---- Execute transition ----
#             output_key = graph.get_output(current_state, input_key)
#             next_state = graph.get_target_state(current_state, input_key)
#             walk.append(f"{input_key}/{output_key}")
#
#             # ---- Update coverage ----
#             current_transition = graph.get_outgoing_transitions_for_state_with_input(
#                 current_state, input_key
#             )
#             visited_transitions.add(current_transition)
#             if next_state not in visited_states:
#                 visited_states.append(next_state)
#             current_state = next_state
#
#             # Continue randomly
#             _continue = rng.uniform(0, 1) >= 0.5
#
#             # Check for completion
#             if len(visited_transitions) == transition_size:
#                 transition_cover = True
#                 print(f"✅ Transition coverage reached ({transition_size} transitions).")
#                 break
#
#         # ---- Add final negative transition ----
#         input_key = rng.choice(graph.input_alphabet)
#         output_key = get_not_exist_output(current_state, input_key, graph, rng)
#         walk.append(f"{input_key}/{output_key}")
#
#         if walk not in negative_walks:
#             negative_walks.append(walk)
#
#     # ============================================================
#     # 🩶 Phase 2: Pure Random Walks — fill until walk count reached
#     # ============================================================
#     # print("Phase 2: Pure random walks until walk limit reached...")
#
#     while len(negative_walks) < negative_walks_size:
#         walk = []
#         current_state = graph.initial_state
#         _continue = True
#
#         while _continue or len(walk) < (graph_size * 2):
#             input_key = rng.choice(graph.input_alphabet)
#             output_key = graph.get_output(current_state, input_key)
#             walk.append(f"{input_key}/{output_key}")
#             current_state = graph.get_target_state(current_state, input_key)
#             _continue = rng.uniform(0, 1) >= 0.5
#
#         # ---- Add final negative transition ----
#         input_key = rng.choice(graph.input_alphabet)
#         output_key = get_not_exist_output(current_state, input_key, graph, rng)
#         walk.append(f"{input_key}/{output_key}")
#
#         if walk not in negative_walks:
#             negative_walks.append(walk)
#
#     # ============================================================
#     # 🧾 Diagnostics
#     # ============================================================
#     if len(visited_states) < graph_size:
#         print(
#             f"Warning: generated walks did not visit all states "
#             f"({len(visited_states)} of {graph_size})."
#         )
#     if len(visited_transitions) < transition_size:
#         print(
#             f"Warning: not all transitions were covered "
#             f"({len(visited_transitions)} of {transition_size})."
#         )
#
#     return negative_walks


def get_not_exist_output(state, input_key, graph, random_variable):
    actual_output_key = graph.get_output(state, input_key)
    output_list_exclude_actual_output = [output for output in graph.output_alphabet if output != actual_output_key]
    output_list_exclude_actual_output.sort()
    random_not_exist_output_key = f'{random_variable.choice(output_list_exclude_actual_output)}'
    return random_not_exist_output_key

def split_into_evaluation_and_training_lists(walks, evaluation_walks_size=30, seed=42):
    rng = random.Random(seed)
    walks_copy = walks[:]
    rng.shuffle(walks_copy)
    Evaluation_walks = walks_copy[:evaluation_walks_size]
    Training_walks = walks_copy[evaluation_walks_size:]
    return Training_walks, Evaluation_walks

def write_walks_to_file(training_pos_walks, training_neg_walks, test_pos_walks, test_neg_walks, filename):
    with open(filename, 'w') as file:
        file.write(f'__________Learning_Positive Traces_________\n')
        for walk in training_pos_walks:
            walk_str = to_sting_sperated_by_comma(walk)
            file.write(f'{walk_str}\n')
        file.write(f'__________Learning_Negative Traces_________\n')
        for walk in training_neg_walks:
            walk_str = to_sting_sperated_by_comma(walk)
            file.write(f'{walk_str}\n')
        file.write(f'__________EVALUATION_Positive Traces_________\n')
        for walk in test_pos_walks:
            walk_str = to_sting_sperated_by_comma(walk)
            file.write(f'{walk_str}\n')
        file.write(f'__________EVALUATION_Negative Traces_________\n')
        for walk in test_neg_walks:
            walk_str = to_sting_sperated_by_comma(walk)
            file.write(f'{walk_str}\n')

def to_sting_sperated_by_comma(walk):
    walk_str = ''
    for i in range(len(walk)):
        label = walk[i]
        walk_str += label
        if i != len(walk) - 1:
            walk_str += ', '
    return walk_str

def generate_neg_test_walks(graph, seed_value, neg_test_walks_size, neg_training_walks):
    # this neg walk consider the sink state as a reject state.
    # the neg-walk must not loop around the sink state
    rng = random.Random(seed_value)
    sink_states = graph.find_sink_state()
    negative_walks = []
    graph_size = len(graph.get_all_states())
    while len(negative_walks) < neg_test_walks_size:
        walk = []
        from_state = graph.initial_state
        _continue = True
        while _continue or len(walk) < (graph_size*2):
            input_key = f'{rng.choice(graph.input_alphabet)}'
            to_state = graph.get_target_state(from_state, input_key)
            if to_state in sink_states:
                _continue = True
            else:
                output_key = graph.get_output(from_state, input_key)
                walk.append(f'{input_key}/{output_key}')
                from_state = to_state
                _continue = rng.uniform(0, 1) >= 0.5
        # generate the last transition that makes the walk negative. (add not exsitiing transition to the walk)
        reject_transition = ''
        input_key = f'{rng.choice(graph.input_alphabet)}'
        to_state = graph.get_target_state(from_state, input_key)
        if to_state in sink_states:
            output_key = graph.get_output(from_state, input_key)
            reject_transition = f'{input_key}/{output_key}'
        else:
            output_key = get_not_exist_output(from_state, input_key, graph, rng)
            reject_transition = f'{input_key}/{output_key}'
        walk.append(reject_transition)

        if walk not in negative_walks and walk not in neg_training_walks:
            negative_walks.append(walk)
    return negative_walks

def generate_neg_test_walks_short_length(graph, seed_value, neg_test_walks_size, neg_training_walks):
    # this neg walk consider the sink state as a reject state.
    # the neg-walk must not loop around the sink state
    rng = random.Random(seed_value)
    sink_states = graph.find_sink_state()
    negative_walks = []
    graph_size = len(graph.get_all_states())
    while len(negative_walks) < neg_test_walks_size:
        walk = []
        from_state = graph.initial_state
        _continue = True
        # Parameters: (left_bound, right_bound, mode)
        # length_of_walk = rng.triangular(graph_size / 2, graph_size * 2, graph_size)
        length_of_walk = rng.uniform(graph_size / 2, graph_size * 2)
        while _continue or len(walk) < length_of_walk:
            input_key = f'{rng.choice(graph.input_alphabet)}'
            to_state = graph.get_target_state(from_state, input_key)
            if to_state in sink_states:
                _continue = True
            else:
                output_key = graph.get_output(from_state, input_key)
                walk.append(f'{input_key}/{output_key}')
                from_state = to_state
                _continue = rng.uniform(0, 1) >= 0.5
        # generate the last transition that makes the walk negative. (add not exsitiing transition to the walk)
        reject_transition = ''
        input_key = f'{rng.choice(graph.input_alphabet)}'
        to_state = graph.get_target_state(from_state, input_key)
        if to_state in sink_states:
            output_key = graph.get_output(from_state, input_key)
            reject_transition = f'{input_key}/{output_key}'
        else:
            output_key = get_not_exist_output(from_state, input_key, graph, rng)
            reject_transition = f'{input_key}/{output_key}'
        walk.append(reject_transition)

        if walk not in negative_walks and walk not in neg_training_walks:
            negative_walks.append(walk)
    return negative_walks

def generate_pos_test_walks(positive_walks_size, graph, seed_value, training_pos_walks=[]):
    # this pos walk consider the sink state as a reject state.
    # positive walks that are not neccessarily cover all transitions and states

    rng = random.Random(seed_value)
    sink_states = graph.find_sink_state()
    positive_walks = []
    graph_size = len(graph.get_all_states())
    while len(positive_walks) < positive_walks_size :
        walk = []
        from_state = graph.initial_state
        _continue = True
        while _continue or len(walk) < (graph_size*2):
            input_key = f'{rng.choice(graph.input_alphabet)}'
            to_state = graph.get_target_state(from_state, input_key)
            if to_state in sink_states:
                _continue = True
            else:
                output_key = graph.get_output(from_state, input_key)
                walk.append(f'{input_key}/{output_key}')
                from_state = to_state
                _continue = rng.uniform(0, 1) >= 0.5
        if walk not in positive_walks:
            positive_walks.append(walk)

        if walk not in positive_walks and walk not in training_pos_walks:
            positive_walks.append(walk)
    return positive_walks

def generate_pos_test_walks_short_length(positive_walks_size, graph, seed_value, training_pos_walks=[]):
    # this pos walk consider the sink state as a reject state.
    # positive walks that are not neccessarily cover all transitions and states

    rng = random.Random(seed_value)
    sink_states = graph.find_sink_state()
    positive_walks = []
    graph_size = len(graph.get_all_states())
    while len(positive_walks) < positive_walks_size :
        walk = []
        from_state = graph.initial_state
        _continue = True
        # Parameters: (left_bound, right_bound, mode)
        # length_of_walk = rng.triangular(graph_size / 2, graph_size * 2, graph_size)
        length_of_walk = rng.uniform(graph_size / 2, graph_size * 2)
        while _continue or len(walk) < length_of_walk:
            input_key = f'{rng.choice(graph.input_alphabet)}'
            to_state = graph.get_target_state(from_state, input_key)
            if to_state in sink_states:
                _continue = True
            else:
                output_key = graph.get_output(from_state, input_key)
                walk.append(f'{input_key}/{output_key}')
                from_state = to_state
                _continue = rng.uniform(0, 1) >= 0.5
        if walk not in positive_walks:
            positive_walks.append(walk)

        if walk not in positive_walks and walk not in training_pos_walks:
            positive_walks.append(walk)
    return positive_walks

def generate_prefixed_closed_negative_walks_transition_cover_minimal(
    negative_walks_size, graph, seed_value, epsilon=0.2
):
    """
    Generate negative walks using two phases:
      1. Guided random walk (ε-greedy) until transition coverage is achieved.
      2. Pure random walks until negative_walks_size is reached.
    Each generated walk is a valid continuous path (no teleportation).
    """

    rng = random.Random(seed_value)
    negative_walks = []
    visited_states = [graph.initial_state]
    visited_transitions = set()

    graph_size = len(graph.get_all_states())
    transition_size = len(graph.get_all_transitions())
    transition_cover = False

    # ============================================================
    # 🩵 Phase 1: Guided Random Walk — reach transition coverage
    # ============================================================
    # print("Phase 1: Guided random walk until transition coverage...")

    while not transition_cover:
        walk = []
        current_state = graph.initial_state
        _continue = True

        add_new_transition = False

        while _continue or len(walk) < (graph_size*2):
            outgoing_transitions = graph.get_outgoing_transitions_for_state(current_state)
            uncovered = [t for t in outgoing_transitions if t not in visited_transitions]

            # ---- Input selection ----
            if uncovered and rng.random() > epsilon:
                # Exploit uncovered transitions
                chosen_transition = rng.choice(uncovered)
                input_key = chosen_transition.input_key
            else:
                # Explore randomly
                input_key = rng.choice(graph.input_alphabet)

            # ---- Execute transition ----
            output_key = graph.get_output(current_state, input_key)
            next_state = graph.get_target_state(current_state, input_key)
            walk.append(f"{input_key}/{output_key}")

            # ---- Update coverage ----
            current_transition = graph.get_outgoing_transitions_for_state_with_input(
                current_state, input_key
            )
            if current_transition not in visited_transitions:
                add_new_transition = True
            visited_transitions.add(current_transition)
            if next_state not in visited_states:
                visited_states.append(next_state)
            current_state = next_state

            # Continue randomly
            _continue = rng.uniform(0, 1) >= 0.5

            # Check for completion
            if len(visited_transitions) == transition_size:
                transition_cover = True
                print(f"✅ Transition coverage reached ({transition_size} transitions).")
                break

        # ---- Add final negative transition ----
        input_key = rng.choice(graph.input_alphabet)
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f"{input_key}/{output_key}")

        if walk not in negative_walks and add_new_transition:
            negative_walks.append(walk)

    # ============================================================
    # 🩶 Phase 2: Pure Random Walks — fill until walk count reached
    # ============================================================
    # print("Phase 2: Pure random walks until walk limit reached...")

    while len(negative_walks) < negative_walks_size:
        walk = []
        current_state = graph.initial_state
        _continue = True

        while _continue or len(walk) < (graph_size * 2):
            input_key = rng.choice(graph.input_alphabet)
            output_key = graph.get_output(current_state, input_key)
            walk.append(f"{input_key}/{output_key}")
            current_state = graph.get_target_state(current_state, input_key)
            _continue = rng.uniform(0, 1) >= 0.5

        # ---- Add final negative transition ----
        input_key = rng.choice(graph.input_alphabet)
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f"{input_key}/{output_key}")

        if walk not in negative_walks:
            negative_walks.append(walk)

    # ============================================================
    # 🧾 Diagnostics
    # ============================================================
    if len(visited_states) < graph_size:
        print(
            f"Warning: generated walks did not visit all states "
            f"({len(visited_states)} of {graph_size})."
        )
    if len(visited_transitions) < transition_size:
        print(
            f"Warning: not all transitions were covered "
            f"({len(visited_transitions)} of {transition_size})."
        )

    return negative_walks

def generate_prefixed_closed_negative_walks_state_cover_minimal(
    negative_walks_size, graph, seed_value, epsilon=0.2
):
    """
    Generate negative walks using two phases:
      1. Guided random walk (ε-greedy) until transition coverage is achieved.
      2. Pure random walks until negative_walks_size is reached.
    Each generated walk is a valid continuous path (no teleportation).
    """

    rng = random.Random(seed_value)
    negative_walks = []
    visited_states = [graph.initial_state]
    visited_transitions = set()

    graph_size = len(graph.get_all_states())
    transition_size = len(graph.get_all_transitions())
    state_cover = False

    # ============================================================
    # 🩵 Phase 1: Guided Random Walk — reach transition coverage
    # ============================================================
    # print("Phase 1: Guided random walk until transition coverage...")

    while not state_cover:
        walk = []
        current_state = graph.initial_state
        _continue = True

        add_new_state = False

        while _continue or len(walk) < (graph_size):
            children = graph.get_children(current_state)
            uncovered = [s for s in children if s not in visited_states]

            # ---- Input selection ----
            if uncovered and rng.random() > epsilon:
                # Exploit uncovered transitions
                next_state = rng.choice(uncovered)
            else:
                # Explore randomly
                next_state = rng.choice(children)

            # ---- Execute transition ----
            trnsitions_between_states = graph.graph[current_state][next_state]
            current_transition = rng.choice(trnsitions_between_states)
            walk.append(f"{current_transition.input_key}/{current_transition.output_key}")

            visited_transitions.add(current_transition)
            if next_state not in visited_states:
                visited_states.append(next_state)
                add_new_state = True
            current_state = next_state

            # Continue randomly
            _continue = rng.uniform(0, 1) >= 0.5

            # Check for completion
            if len(visited_states) == graph_size:
                state_cover = True
                print(f"✅ State coverage reached ({graph_size} transitions).")
                break

        # ---- Add final negative transition ----
        input_key = rng.choice(graph.input_alphabet)
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f"{input_key}/{output_key}")

        if walk not in negative_walks and add_new_state:
            negative_walks.append(walk)

    # ============================================================
    # 🩶 Phase 2: Pure Random Walks — fill until walk count reached
    # ============================================================
    # print("Phase 2: Pure random walks until walk limit reached...")

    while len(negative_walks) < negative_walks_size:
        walk = []
        current_state = graph.initial_state
        _continue = True

        while _continue or len(walk) < (graph_size):
            input_key = rng.choice(graph.input_alphabet)
            output_key = graph.get_output(current_state, input_key)
            walk.append(f"{input_key}/{output_key}")
            current_state = graph.get_target_state(current_state, input_key)
            _continue = rng.uniform(0, 1) >= 0.5

        # ---- Add final negative transition ----
        input_key = rng.choice(graph.input_alphabet)
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f"{input_key}/{output_key}")

        if walk not in negative_walks:
            negative_walks.append(walk)

    # ============================================================
    # 🧾 Diagnostics
    # ============================================================
    if len(visited_states) < graph_size:
        print(
            f"Warning: generated walks did not visit all states "
            f"({len(visited_states)} of {graph_size})."
        )
    if len(visited_transitions) < transition_size:
        print(
            f"Warning: not all transitions were covered "
            f"({len(visited_transitions)} of {transition_size})."
        )

    return negative_walks

def add_more_random_prefixed_closed_traces(minimum_neg_walks, negative_walks_size, seed_value, graph):
    rng = random.Random(seed_value)
    negative_walks = minimum_neg_walks
    visited_states = [graph.initial_state]
    graph_size = len(graph.get_all_states())
    while len(negative_walks) < negative_walks_size:
        walk = []
        current_state = graph.initial_state
        _continue = True
        while _continue or len(walk) < (graph_size * 2):
            input_key = f'{rng.choice(graph.input_alphabet)}'
            output_key = graph.get_output(current_state, input_key)
            walk.append(f'{input_key}/{output_key}')
            current_state = graph.get_target_state(current_state, input_key)
            if current_state not in visited_states:
                visited_states.append(current_state)
            _continue = rng.uniform(0, 1) >= 0.5
        # generate the last transition that makes the walk negative. (add not exsitiing transition to the walk)
        input_key = f'{rng.choice(graph.input_alphabet)}'
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f'{input_key}/{output_key}')

        if walk not in negative_walks:
            negative_walks.append(walk)
    return negative_walks