from Graph import Graph
from State import State





def test_get_outgoingTransition():
    g = Graph()
    state0 = State('S0', 'accepted', True)
    state1 = State('S1', 'accepted', False)
    g.graph = {state0: {state1:['TansitionA'], state0:['TansitionB']}
             }
    g.graph[state1] = {state0:['TransitionC']}

    g.print_graph()

    print(f'outgoing transitions for {state0}: {g.get_outgoing_transitions(state0)}')

def test_get_IncomingTransition():
    g = Graph()
    state0 = State('S0', 'accepted', True)
    state1 = State('S1', 'accepted', False)
    g.graph = {state0: {state1:['TansitionA'], state0:['TansitionB']}
             }
    g.graph[state1] = {state0:['TransitionC']}

    g.print_graph()

    print(f'incoming transitions to {state0}: {g.get_incoming_transitions(state0)}')

if __name__ == "__main__":
    test_get_outgoingTransition()
    test_get_IncomingTransition()
