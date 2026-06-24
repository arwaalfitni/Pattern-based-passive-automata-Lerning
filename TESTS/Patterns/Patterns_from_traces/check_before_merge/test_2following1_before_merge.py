import unittest

from Basic_objects.DISJOINTSETS import DisjointSet
from Basic_objects.Graph import Graph
from Basic_objects.State import State
from Basic_objects.Transition import Transition
from Basic_objects.Tree import Tree
from Patterns.pattern_from_traces.check_after_merge import is_violate_pattern_2NotFollowing1


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.S1 = State('S1', 'accepted', isInitial=True)
        self.S2 = State('S2', 'accepted')
        self.S3 = State('S3', 'accepted')
        S4 = State('S4', 'accepted')
        S5 = State('S5', 'rejected')
        self.S6 = State('S6', 'accepted')
        S7 = State('S7', 'accepted')
        S8 = State('S8', 'accepted')
        S9 = State('S9', 'accepted')

        T_S1_S2 = Transition(self.S1, self.S2, 'a', '1')
        T_S2_S3 = Transition(self.S2, self.S3, 'a', '2')
        T_S3_S4 = Transition(self.S3, S4, 'b', '2')
        T_S4_S5 = Transition(S4, S5, 'b', '1')
        T_S1_S6 = Transition(self.S1, self.S6, 'c', '1')
        T_S6_S7 = Transition(self.S6, S7, 'a', '2')
        T_S7_S8 = Transition(S7, S8, 'b', '2')
        T_S8_S9 = Transition(S8, S9, 'c', '1')


        G = Graph()
        G.set_initial_state(self.S1)
        G.set_input_alphabet(['a', 'b', 'c'])
        G.set_output_alphabet(['1', '2'])
        G.set_alphabet(['a/1', 'b/1', 'c/1', 'a/2', 'b/2'])
        G.graph = {
            self.S1: {self.S2: [T_S1_S2], self.S6: [T_S1_S6]},
            self.S2: {self.S3: [T_S2_S3]},
            self.S3: {S4: [T_S3_S4]},
            S4: {S5: [T_S4_S5]},
            S5: {},
            self.S6: {S7: [T_S6_S7]},
            S7: {S8: [T_S7_S8]},
            S8: {S9: [T_S8_S9]}
        }
        self.apta = Tree()
        self.apta.G = G

        self.pattern_map = {('a/1', 'a/2'):
                           {'followed_by': {'b/2': 100.0},
                            'not_followed_by': ['a/1', 'b/1', 'c/1', 'a/2'],
                            'percentage_of_appearance': 12.5},
                       ('a/2', 'b/2'):
                           {'followed_by': {'c/1': 50.0},
                            'not_followed_by': ['a/1', 'b/1', 'a/2', 'b/2'],
                            'percentage_of_appearance': 25.0},
                       ('b/2', 'b/1'):
                           {'followed_by': {},
                            'not_followed_by': ['a/1', 'b/1', 'c/1', 'a/2', 'b/2'],
                            'percentage_of_appearance': 12.5},
                       ('b/2', 'c/1'):
                           {'followed_by': {},
                            'not_followed_by': ['a/1', 'b/1', 'c/1', 'a/2', 'b/2'],
                            'percentage_of_appearance': 12.5},
                       ('c/1', 'a/2'):
                           {'followed_by': {'b/2': 100.0},
                            'not_followed_by': ['a/1', 'b/1', 'c/1', 'a/2'],
                            'percentage_of_appearance': 12.5}
                       }

    def test_violatingCase(self):
        ds=DisjointSet()
        for s in self.apta.G.get_all_states():
            ds.make_set(s)
        ds.union(self.S1, self.S3)

        result, violated_label = is_violate_pattern_2NotFollowing1(ds, self.pattern_map, self.apta.G)
        self.assertEqual(result, True)
        self.assertEqual(violated_label, ('a/1', 'a/2', {'c/1', 'a/1'}))

    def test_NotViolatingCase(self):
        ds=DisjointSet()
        for s in self.apta.G.get_all_states():
            ds.make_set(s)
        ds.union(self.S2, self.S6)

        result, violated_label = is_violate_pattern_2NotFollowing1(ds, self.pattern_map, self.apta.G)
        self.assertEqual(result, False)
        self.assertEqual(violated_label, None)

    def test_sequenceNotInMap(self):
        ds=DisjointSet()
        for s in self.apta.G.get_all_states():
            ds.make_set(s)
        ds.union(self.S1, self.S2)

        result, violated_label = is_violate_pattern_2NotFollowing1(ds, self.pattern_map, self.apta.G)
        self.assertEqual(result, False)
        self.assertEqual(violated_label, None)

if __name__ == '__main__':
    unittest.main()
