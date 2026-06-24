def bias_merging_score (ds, exp_map, graph_after_merge):

    sets = ds.get_sets()
    for target, sources in sets.items():
        if len(sources) > 1:
            in_trans = graph_after_merge.get_incoming_transitions(target)
            out_trans = graph_after_merge.get_outgoing_transitions_for_state(target)

            for it in in_trans:
                if it.label in exp_map.keys():
                    for ot in out_trans:
                        # if ot.label in exp_map[it.label]['followed_by'].keys():
                        #     increase_score(ds, exp_map[it.label]['followed_by'][ot.label])
                        if ot.label in exp_map[it.label]['not_followed_by'] and ot.to_state.type == ('accepted'):
                            decrease_score(ds, exp_map[it.label]['percentage_of_appearance'])


# def increase_score(ds, percentage):
#     if ds.merging_score == 0:
#         INCREASE_BY = round(1 * (percentage / 100), 2)
#     else:
#         INCREASE_BY = round(ds.merging_score *(percentage/100), 2)
#     ds.biased_by +=INCREASE_BY

def decrease_score(ds, percentage):
    if ds.merging_score == 0:
        DECREASE_BY = round(1 * (percentage / 100), 2)
    else:
        DECREASE_BY = round(ds.merging_score * (percentage / 100), 2)
    ds.biased_by -= DECREASE_BY

def is_violate_pattern(ds, pattern_map, graph_after_merge):
    sets = ds.get_sets()
    for target, sources in sets.items():
        if len(sources) > 1:
            in_trans = graph_after_merge.get_incoming_transitions(target)
            out_trans = graph_after_merge.get_outgoing_transitions_for_state(target)

            for it in in_trans:
                if it.label in pattern_map.keys():
                    for ot in out_trans:
                        if ot.label in pattern_map[it.label]['not_followed_by'] and ot.to_state.type == ('accepted'):
                            return True, it.label
    return False, None
#check violation without performing the merge
# def is_violate_pattern_1NotFollowing1(ds, pattern_map, graph_before_merge):
#     sets = ds.get_sets()
#     for target, members in sets.items():
#         if len(members) <= 1:
#             continue
#         in_trans = graph_before_merge.get_incoming_transitions_for_list_of_states(members)
#         out_trans = graph_before_merge.get_outgoing_transitions_for_list_of_states(None, members)
#
#         for it in in_trans:
#             if it.label in pattern_map.keys():
#                 for ot in out_trans:
#                     if ot.label in pattern_map[it.label]['not_followed_by'] and ot.to_state.type == ('accepted'):
#                         return True, it.label
#     return False, None

# _optimized
def is_violate_pattern_1NotFollowing1(ds, pattern_map, graph_before_merge):
    # 1. Pre-process pattern_map into a fast lookup (Set for O(1) checks)
    # Mapping: { incoming_label: set(forbidden_outgoing_labels) }
    fast_patterns = {
        label: set(data.get('not_followed_by', []))
        for label, data in pattern_map.items()
    }

    sets = ds.get_sets()

    for target, members in sets.items():
        if len(members) <= 1:
            continue

        # 2. Get transitions once per merged set
        in_trans = graph_before_merge.get_incoming_transitions_for_list_of_states(members)
        out_trans = graph_before_merge.get_outgoing_transitions_for_list_of_states(None, members)

        # 3. Pre-filter outgoing transitions that lead to 'accepted'
        # Store as a set of labels for instant intersection
        accepted_out_labels = {
            ot.label for ot in out_trans
            if ot.to_state.type == 'accepted'
        }

        if not accepted_out_labels:
            continue

        # 4. Check for violations
        for it in in_trans:
            # Get the forbidden set for this specific incoming label
            forbidden_set = fast_patterns.get(it.label)

            if forbidden_set:
                # Use Set Intersection: find if any accepted_out_label is in forbidden_set
                # This replaces the entire inner 'for ot in out_trans' loop
                if not accepted_out_labels.isdisjoint(forbidden_set):
                    return True, it.label

    return False, None
def is_violate_pattern_not_proceed(ds, pattern_map, graph_before_merge):
    sets = ds.get_sets()
    for target, sources in sets.items():
        if len(sources) > 1:
            in_trans = graph_before_merge.get_incoming_transitions(target)
            out_trans = graph_before_merge.get_outgoing_transitions_for_list_of_states(target, sources)

            for ot in out_trans:
                if ot.label in pattern_map.keys():
                    for it in in_trans:
                        if it.label in pattern_map[ot.label]['not_proceed_by']:
                            return True, it.label
    return False, None


def is_violate_pattern_2NotFollowing1(ds, pattern_map, graph_before_merge):
    # Pre-calculate pattern lookup for O(1) access
    # Maps step2 -> {step1: [forbidden_next_steps]}
    fast_pattern = {}
    for (s1, s2), data in pattern_map.items():
        if s2 not in fast_pattern:
            fast_pattern[s2] = {}
        fast_pattern[s2][s1] = set(data.get('not_followed_by', []))

    sets = ds.get_sets()

    for target_root, members in sets.items():
        if len(members) <= 1:
            continue

        # Get all transitions involving this merged set once
        in_trans = graph_before_merge.get_incoming_transitions_for_list_of_states(members)
        out_trans = graph_before_merge.get_outgoing_transitions_for_list_of_states(None, members)

        # Identify if any outgoing transition leads to an accepted state
        # Store as a set of labels for O(1) violation checking
        forbidden_candidates = {ot.label for ot in out_trans if ot.to_state.type == 'accepted'}

        if not forbidden_candidates:
            continue

        for it in in_trans:
            # If the current incoming transition label matches a 'step2' in our patterns
            if it.label in fast_pattern:
                # Look at the state BEFORE the current incoming transition
                prev_transitions = graph_before_merge.get_incoming_transitions(it.from_state)

                for prev_it in prev_transitions:
                    # Check if (prev_it.label, it.label) is a registered pattern
                    forbidden_set = fast_pattern[it.label].get(prev_it.label)

                    if forbidden_set:
                        # Intersection check: does any outgoing label exist in the forbidden list?
                        violation = forbidden_candidates.intersection(forbidden_set)
                        if violation:
                            return True, (prev_it.label, it.label, violation)

    return False, None

def is_violate_pattern_1NotFollowing1_check_all_states(pattern_map, graph):
    violate = False
    violation_map = {}
    violated_pattern_count = 0
    # 1. Pre-process pattern_map into a fast lookup (Set for O(1) checks)
    # Mapping: { incoming_label: set(forbidden_outgoing_labels) }
    fast_patterns = {
        label: set(data.get('not_followed_by', []))
        for label, data in pattern_map.items()
    }

    for state in graph.get_all_states():
        # 1. Get transitions once per merged set
        in_trans = graph.get_incoming_transitions(state)
        out_trans = graph.get_outgoing_transitions_for_state(state)

        # 2. Pre-filter ingoing transitions
        # Store as a set of labels for instant intersection
        in_labels = {it.label for it in in_trans}

        if not in_labels:
            continue

        # 3. Pre-filter outgoing transitions that lead to 'accepted'
        # Store as a set of labels for instant intersection
        accepted_out_labels = {
            ot.label for ot in out_trans
            if ot.to_state.type == 'accepted'
        }

        if not accepted_out_labels:
            continue

        # 4. Check for violations
        for in_label in in_labels:
            # Get the forbidden set for this specific incoming label
            forbidden_set = fast_patterns.get(in_label)

            if forbidden_set:
                # Use Set Intersection: find if any accepted_out_label is in forbidden_set
                # This replaces the entire inner 'for ot in out_trans' loop
                if not accepted_out_labels.isdisjoint(forbidden_set):
                    violate=True
                    violated_out_labels = accepted_out_labels & forbidden_set
                    if state.label not in violation_map:
                        violation_map[in_label] = set(violated_out_labels)
                    else:
                        violation_map[in_label].add(violated_out_labels)

    return violate, violation_map