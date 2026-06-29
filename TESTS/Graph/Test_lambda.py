from Graph import Graph
from State import State


def test_get_output():
    g = Graph()
    state0 = State('S0', 'accepted', True)
    state1 = State('S1', 'accepted', False)
    input = 'TansitionA'
    g.graph = {state0: {state1:['TansitionA/outputA', 'TansitionC/outputA'], state0:['TansitionB/outputB']}
             }
    g.graph[state1] = {state0:['TransitionC/outputA']}

    g.print_graph()

    print(f'output for {state0} and  {input}: {g.lambdaFunction(state0,input)}')

if __name__=="__main__":
    test_get_output()