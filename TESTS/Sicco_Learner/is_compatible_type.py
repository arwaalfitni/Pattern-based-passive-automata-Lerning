import unittest

from Basic_objects.Graph import Graph
from Basic_objects.State import State
from Basic_objects.Transition import Transition
from Basic_objects.Tree import Tree
from Learners.Sicco_Learner import Sicco_Learner


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.R1 = State('R1','accepted', isInitial=True)
        self.R2 = State('R2','accepted')
        self.R3 = State('R3','accepted')
        self.B1 = State('B1'); self.B2 = State('B2')
        self.W1 = State('W1','accepted')
        self.W2 = State('W2','rejected')
        self.W3 = State('W3','rejected')

        T_R1_R3 = Transition(self.R1, self.R3, 'a', '1')
        T_R1_R2 = Transition(self.R1, self.R2, 'b', '2')
        T_R2_R3 = Transition(self.R2, self.R3, 'a', '2')
        T_R2_R2 = Transition(self.R2, self.R2, 'b', '1')
        T_R3_B2 = Transition(self.R3, self.B2, 'a', '1')
        T_B2_W3 = Transition(self.B2, self.W3, 'b', '2')
        T_R2_B1 = Transition(self.R2, self.B1, 'c', '1')
        T_B1_W1 = Transition(self.B1, self.W1, 'a', '1')
        T_W1_W2 = Transition(self.W1, self.W2, 'c', '1')

        G = Graph()
        G.set_initial_state(self.R1)
        G.set_alphabet(['a', 'b', 'c'])
        G.set_output_alphabet(['1', '2'])
        G.graph={
            self.R1:{self.R2:[T_R1_R2], self.R3:[T_R1_R3]},
            self.R2:{self.R2:[T_R2_R2], self.R3:[T_R2_R3], self.B1:[T_R2_B1]},
            self.R3:{self.B2:[T_R3_B2]},
            self.B1:{self.W1:[T_B1_W1]},
            self.B2:{self.W3:[T_B2_W3]},
            self.W1:{self.W2:[T_W1_W2]},
            self.W2:{},
            self.W3:{}
        }
        # graph_to_dot(G, 'test_G.dot')
        # dot_to_png('test_G.dot', 'test_G.png')
        apta = Tree(); apta.G=G
        self.sicco_learner = Sicco_Learner(apta)
        self.sicco_learner.setup('')
        self.sicco_learner.red_states = [self.R1, self.R2, self.R3]
        self.sicco_learner.blue_states = [self.B1, self.B2]

    def test_all_accept(self):
        compatible, list_type = self.sicco_learner.is_compatible_type([self.R1, self.R2, self.W1])
        self.assertEqual(compatible, True)
        self.assertEqual(list_type, 'accepted')# add assertion here
    def test_all_reject(self):
        compatible, list_type = self.sicco_learner.is_compatible_type([self.W2, self.W3])
        self.assertEqual(compatible, True)
        self.assertEqual(list_type, 'rejected')
    def test_accept_reject(self):
        compatible, list_type = self.sicco_learner.is_compatible_type([self.R1, self.R2, self.W2])
        self.assertEqual(compatible, False)
        self.assertEqual(list_type, 'unlabeled')
    def test_accept_unlabeled(self):
        compatible, list_type = self.sicco_learner.is_compatible_type([self.R1, self.B2, self.B1])
        self.assertEqual(compatible, True)
        self.assertEqual(list_type, 'accepted')
    def test_reject_unlabeled(self):
        compatible, list_type = self.sicco_learner.is_compatible_type([self.W2, self.B2, self.B1])
        self.assertEqual(compatible, True)
        self.assertEqual(list_type, 'rejected')
    def test_all_unlabeled(self):
        compatible, list_type = self.sicco_learner.is_compatible_type([self.B2, self.B1])
        self.assertEqual(compatible, True)
        self.assertEqual(list_type, 'unlabeled')


if __name__ == '__main__':
    unittest.main()
