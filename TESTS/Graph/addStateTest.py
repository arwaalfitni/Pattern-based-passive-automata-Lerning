# import unittest
#
# from Graph import Graph
# from State import State
#
#
# class TestGraphsEquality(unittest.TestCase):
#     def setUp(self) -> None:
#         self.graph = Graph('S0')
#
#     def test_addStateToEmptyGraph(self):
#         state1 = State('S1', 'accepted', False)
#         self.graph.addState(state1)
#
#         ActualGraph = {}
#
# if __name__ == "__main__":
#     unittest.main()


from Graph import Graph
from State import State


def test_addStateToEmptyGraph(graph):
    state0 = State('S0', 'accepted', False)
    graph.addState(state0)

def test_addStateToNonEmptyGraph(graph):
    state1 = State('S1', 'accepted', False)
    graph.addState(state1)


if __name__ == "__main__":
    graph = Graph()
    test_addStateToEmptyGraph(graph)
    test_addStateToNonEmptyGraph(graph)
    graph.print_graph()