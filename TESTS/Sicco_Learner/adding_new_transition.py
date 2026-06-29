import unittest

from Basic_objects.Graph import Graph
from Basic_objects.State import State
from Basic_objects.Transition import Transition
from Basic_objects.Tree import Tree
from Form_converter.GraphObj_DotFile_converter import graph_to_dot
from Form_converter.dot_to_png import dot_to_png
from Learners.Sicco_Learner import Sicco_Learner


class MyTestCase(unittest.TestCase):
    
    def setUp(self):
        self.R1 = State('R1', isInitial=True); self.R2 = State('R2'); self.R3 = State('R3')
        self.B1 = State('B1'); self.B2 = State('B2')
        self.W1 = State('W1'); W2 = State('W2'); W3 = State('W3')

        T_R1_R3 = Transition(self.R1, self.R3, 'a', '1')
        T_R1_R2 = Transition(self.R1, self.R2, 'b', '2')
        T_R2_R3 = Transition(self.R2, self.R3, 'a', '2')
        T_R2_R2 = Transition(self.R2, self.R2, 'b', '1')
        T_R3_B2 = Transition(self.R3, self.B2, 'a', '1')
        T_B2_W3 = Transition(self.B2, W3, 'b', '2')
        T_R2_B1 = Transition(self.R2, self.B1, 'c', '1')
        T_B1_W1 = Transition(self.B1, self.W1, 'a', '1')
        T_W1_W2 = Transition(self.W1, W2, 'c', '1')

        G = Graph()
        G.set_initial_state(self.R1)
        G.set_alphabet(['a', 'b', 'c'])
        G.set_output_alphabet(['1', '2'])
        G.graph={
            self.R1:{self.R2:[T_R1_R2], self.R3:[T_R1_R3]},
            self.R2:{self.R2:[T_R2_R2], self.R3:[T_R2_R3], self.B1:[T_R2_B1]},
            self.R3:{self.B2:[T_R3_B2]},
            self.B1:{self.W1:[T_B1_W1]},
            self.B2:{W3:[T_B2_W3]},
            self.W1:{W2:[T_W1_W2]},
            W2:{},
            W3:{}
        }
        # graph_to_dot(G, 'test_G.dot')
        # dot_to_png('test_G.dot', 'test_G.png')
        apta = Tree(); apta.G=G
        self.sicco_learner = Sicco_Learner(apta)
        self.sicco_learner.setup('')
        self.sicco_learner.red_states = [self.R1, self.R2, self.R3]
        self.sicco_learner.blue_states = [self.B1, self.B2]


    def test_mergeR1_B1(self):
        result = self.sicco_learner.adding_new_transition(self.R1,self.B1)
        self.assertEqual(result, False)  # R1+B1 = no new info added ==> can be merged by sicco

    def test_mergeR2_B1(self):
        result = self.sicco_learner.adding_new_transition(self.R2, self.B1)
        self.assertEqual(result, False)
        # R2+B1 = no new info added ==> can be merged by sicco; but it must blocked by input compatible

    def test_mergeR3_B1(self):
        result = self.sicco_learner.adding_new_transition(self.R3, self.B1)
        self.assertEqual(result, False) # R3+B1 = no new info added ==> can be merged by sicco;

    def test_mergeR3_B2(self):
        result = self.sicco_learner.adding_new_transition(self.R3, self.B2)
        self.assertEqual(result, True) # R3+B2 = new info added ==> can't be merged by sicco;

    def test_mergeR3_W1(self):
        result = self.sicco_learner.adding_new_transition(self.R3, self.W1)
        self.assertEqual(result, True) # R3+W1 = new info added ==> can't be merged by sicco;


if __name__ == '__main__':
    unittest.main()
