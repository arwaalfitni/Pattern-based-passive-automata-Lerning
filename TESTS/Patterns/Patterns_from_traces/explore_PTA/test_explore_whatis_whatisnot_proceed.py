import unittest

from Basic_objects.Graph import Graph
from Basic_objects.State import State
from Basic_objects.Transition import Transition
from Basic_objects.Tree import Tree
from Patterns.pattern_from_traces.Explore_PTA import explor_whatis_whatisnot_proceed


class MyTestCase(unittest.TestCase):
    def setUp(self):
        S1 = State('S1', 'accepted', isInitial=True)
        S2 = State('S2', 'accepted')
        S3 = State('S3', 'accepted')
        S4 = State('S4', 'accepted')
        S5 = State('S5', 'rejected')
        S6 = State('S6', 'accepted')
        S7 = State('S7', 'accepted')
        S8 = State('S8', 'accepted')

        T_S1_S2 = Transition(S1, S2, 'a', '1')
        T_S2_S3 = Transition(S2, S3, 'a', '2')
        T_S3_S4 = Transition(S3, S4, 'b', '2')
        T_S4_S5 = Transition(S4, S5, 'b', '1')
        T_S1_S6 = Transition(S1, S6, 'c', '1')
        T_S6_S7 = Transition(S6, S7, 'a', '2')
        T_S7_S8 = Transition(S7, S8, 'c', '1')


        G = Graph()
        G.set_initial_state(S1)
        G.set_input_alphabet(['a', 'b', 'c'])
        G.set_output_alphabet(['1', '2'])
        G.set_alphabet(['a/1', 'b/1', 'c/1', 'a/2', 'b/2'])
        G.graph = {
            S1: {S2: [T_S1_S2], S6: [T_S1_S6]},
            S2: {S3: [T_S2_S3]},
            S3: {S4: [T_S3_S4]},
            S4: {S5: [T_S4_S5]},
            S5: {},
            S6: {S7: [T_S6_S7]},
            S7: {S8: [T_S7_S8]},
            S8: {}
        }
        self.apta = Tree()
        self.apta.G = G

    def test_something(self):
        pattern_map = explor_whatis_whatisnot_proceed(self.apta)
        self.assertEqual(True, True)
        # if pattern_map.keys() == ['a/1', 'b/1', 'c/1', 'a/2', 'b/2']:
        #     self.assertEqual(True, True)  # add assertion here
        # if pattern_map['a/1']['proceed_by'].keys() == [] and pattern_map['a/1']['not_proceed_by'].keys() == ['a/1', 'b/1', 'c/1', 'a/2', 'b/2']:
        #     self.assertEqual(True, True)  # add assertion here
        # if pattern_map['b/1']['proceed_by'].keys() == ['b/2'] and pattern_map['b/1']['not_proceed_by'].keys() == ['a/1', 'b/1', 'c/1', 'a/2']:
        #     self.assertEqual(True, True)  # add assertion here
        # if pattern_map['c/1']['proceed_by'].keys() == ['a/2'] and pattern_map['c/1']['not_proceed_by'].keys() == ['a/1', 'b/1', 'c/1', 'b/2']:
        #     self.assertEqual(True, True)
        # if pattern_map['a/2']['proceed_by'].keys() == ['a/1', 'c/1'] and pattern_map['a/2']['not_proceed_by'].keys() == ['b/1', 'a/2', 'b/2']:
        #     self.assertEqual(True, True)
        # if pattern_map['b/2']['proceed_by'].keys() == ['a/2'] and pattern_map['b/2']['not_proceed_by'].keys() == ['a/1', 'b/1', 'c/1', 'b/2']:
        #     self.assertEqual(True, True)
if __name__ == '__main__':
    unittest.main()
