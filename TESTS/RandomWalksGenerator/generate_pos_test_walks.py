import unittest

from Form_converter.GraphObj_DotFile_converter import dot_to_Graph
from RandomWalksGenerator import generate_pos_test_walks


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.ref_graph = dot_to_Graph(f'reference_automata/coffeemachine_reference.dot')
        self.ref_graph.input_alphabet.sort()
    def test_generated_walks_are_pos(self):
        # the last transition in each walk should lead to non-sink state
        sink_state = self.ref_graph.find_sink_state()
        test_pos_walks = generate_pos_test_walks(50, self.ref_graph, 5)
        for walk in test_pos_walks:
            from_state = self.ref_graph.initial_state
            for step in walk:
                input_key, output_key = step.split('/')
                to_state = self.ref_graph.get_target_state(from_state, input_key)
                self.assertNotEqual(sink_state, to_state)
                from_state = to_state


if __name__ == '__main__':
    unittest.main()
