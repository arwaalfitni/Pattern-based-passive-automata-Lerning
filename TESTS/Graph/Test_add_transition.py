from Graph import Graph
from State import State


def test_addTransitionToEmptyGraph():
    graph = Graph()
    state0 = State('S0','unlabeled', True)
    state1 = State('S1', 'unlabeled', False)

    graph.add_transaction(state0, state1, 'TansitionA')
    graph.print_graph()
    pass


def test_addTransitonToNonEmptyGraph():
    graph = Graph()
    state0 = State('S0', 'accepted', True)
    graph.addState(state0)

    state1 = State('S1', 'accepted', False)
    graph.addState(state1)
    graph.add_transaction(graph, state0, state1, 'TansitionA')

    graph.print_graph()

# for a given states S0 and S1, assueme they already have transiton to connect them
# this function add another transition from the same distination to athe same target
def test_addTransiton_multi():
    graph = Graph()
    state0 = State('S0', 'accepted', True)
    graph.addState(state0)

    state1 = State('S1', 'accepted', False)
    graph.addState(state1)
    graph.add_transaction(state0, state1, 'Tansition_A')
    graph.add_transaction(state0, state1, 'Tansition_AA')

    graph.add_transaction(state1, state0, 'Tansition_B')

    graph.print_graph()


if __name__ == "__main__":
    test_addTransitionToEmptyGraph()
    test_addTransiton_multi()
