import unittest

from Basic_objects.Graph import Graph
from Basic_objects.State import State
from Basic_objects.Transition import Transition


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.R1 = State('R1', 'accepted', isInitial=True)
        self.R2 = State('R2', 'accepted')
        self.R3 = State('R3', 'rejected')
        self.B1 = State('B1', 'accepted')
        self.B2 = State('B2', 'accepted')
        self.W1 = State('W1', 'rejected')
        self.W2 = State('W2', 'accepted')
        self.W3 = State('W3', 'accepted')

        self.T_R1_R3 = Transition(self.R1, self.R3, 'a', '1')
        self.T_R1_R2 = Transition(self.R1, self.R2, 'b', '2')
        self.T_R2_R3 = Transition(self.R2, self.R3, 'a', '2')
        self.T_R2_R2 = Transition(self.R2, self.R2, 'b', '1')
        self.T_R3_B2 = Transition(self.R3, self.B2, 'a', '1')
        self.T_B2_W3 = Transition(self.B2, self.W3, 'b', '2')
        self.T_R2_B1 = Transition(self.R2, self.B1, 'c', '1')
        self.T_B1_W1 = Transition(self.B1, self.W1, 'a', '1')
        self.T_W1_W2 = Transition(self.W1, self.W2, 'c', '1')

        self.G = Graph()
        self.G.set_initial_state(self.R1)
        self.G.set_alphabet(['a', 'b', 'c'])
        self.G.set_output_alphabet(['1', '2'])
        self.G.graph = {
            self.R1: {self.R2: [self.T_R1_R2], self.R3: [self.T_R1_R3]},
            self.R2: {self.R2: [self.T_R2_R2], self.R3: [self.T_R2_R3], self.B1: [self.T_R2_B1]},
            self.R3: {self.B2: [self.T_R3_B2]},
            self.B1: {self.W1: [self.T_B1_W1]},
            self.B2: {self.W3: [self.T_B2_W3]},
            self.W1: {self.W2: [self.T_W1_W2]},
            self.W2: {},
            self.W3: {}
        }
    # def test_something(self):
    #     self.G.delete_rejected_states()
    #     self.G.print_graph()
    #     self.assertEqual(True, True)  # add assertion here

    def test_delete_all_rejected(self):
        # T_R1_W1 = Transition(self.R1, self.W1, 'a', '2')
        # self.G.graph[self.R1][self.W1]=[T_R1_W1]
        # self.G.print_graph()
        expected_G = Graph()
        expected_G.set_initial_state(self.R1)
        expected_G.set_alphabet(['a', 'b', 'c'])
        expected_G.set_output_alphabet(['1', '2'])
        expected_G.graph = {
            self.R1: {self.R2: [self.T_R1_R2]},
            self.R2: {self.R2: [self.T_R2_R2], self.B1: [self.T_R2_B1]},
            self.B1: {},
            self.B2: {self.W3: [self.T_B2_W3]},
            self.W2: {},
            self.W3: {}
        }
        self.G.delete_rejected_states()
        # self.G.print_graph()
        result = (self.G == expected_G)
        self.assertTrue(result)

    def test_delete_half_rejected(self):
        expected_G = Graph()
        expected_G.set_initial_state(self.R1)
        expected_G.set_alphabet(['a', 'b', 'c'])
        expected_G.set_output_alphabet(['1', '2'])
        expected_G.graph = {
            self.R1: {self.R2: [self.T_R1_R2]},
            self.R2: {self.R2: [self.T_R2_R2], self.B1: [self.T_R2_B1]},
            self.B1: {self.W1: [self.T_B1_W1]},
            self.B2: {self.W3: [self.T_B2_W3]},
            self.W1: {self.W2: [self.T_W1_W2]},
            self.W2: {},
            self.W3: {}
        }
        self.G.delete_rejected_states('half')
        # self.G.print_graph()
        result = (self.G == expected_G)
        self.assertTrue(result)

    def test_delete_half_rejected_2(self):
        expected_G = Graph()
        expected_G.set_initial_state(self.R1)
        expected_G.set_alphabet(['a', 'b', 'c'])
        expected_G.set_output_alphabet(['1', '2'])
        expected_G.graph = {
            self.R1: {self.R2: [self.T_R1_R2], self.R3: [self.T_R1_R3]},
            self.R2: {self.R2: [self.T_R2_R2], self.R3: [self.T_R2_R3], self.B1: [self.T_R2_B1]},
            self.R3: {self.B2: [self.T_R3_B2]},
            self.B1: {},
            self.B2: {self.W3: [self.T_B2_W3]},
            self.W2: {},
            self.W3: {}
        }
        self.G.delete_rejected_states('half')
        # self.G.print_graph()
        result = (self.G == expected_G)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
