from Basic_objects.Graph import Graph
from Basic_objects.State import State
from Basic_objects.Transition import Transition
from Learners.Sicco_Learner import Sicco_Learner
from Basic_objects.Tree import Tree

def setUp():
    R1 = State('R1', 'accepted', isInitial=True)
    R2 = State('R2', 'accepted')
    R3 = State('R3','accepted')
    R1.color = 'red'; R2.color = 'red'; R3.color = 'red'
    B1 = State('B1','accepted'); B2 = State('B2', 'accepted')
    B1.color = 'blue'; B2.color = 'blue'
    W1 = State('W1','accepted'); W2 = State('W2','accepted'); W3 = State('W3', 'accepted')

    T_R1_R3 = Transition(R1, R3, 'a', '1')
    T_R1_R2 = Transition(R1, R2, 'b', '2')
    T_R2_R3 = Transition(R2, R3, 'a', '2')
    T_R2_R2 = Transition(R2, R2, 'b', '1')
    T_R3_B2 = Transition(R3, B2, 'a', '1')
    T_B2_W3 = Transition(B2, W3, 'b', '2')
    T_R2_B1 = Transition(R2, B1, 'c', '1')
    T_B1_W1 = Transition(B1, W1, 'a', '1')
    T_W1_W2 = Transition(W1, W2, 'c', '1')

    G = Graph()
    G.set_initial_state(R1)
    G.set_alphabet(['a', 'b', 'c'])
    G.set_output_alphabet(['1', '2'])
    G.graph = {
        R1: {R2: [T_R1_R2], R3: [T_R1_R3]},
        R2: {R2: [T_R2_R2], R3: [T_R2_R3], B1: [T_R2_B1]},
        R3: {B2: [T_R3_B2]},
        B1: {W1: [T_B1_W1]},
        B2: {W3: [T_B2_W3]},
        W1: {W2: [T_W1_W2]},
        W2: {},
        W3: {}
    }
    # graph_to_dot(G, 'test_G.dot')
    # dot_to_png('test_G.dot', 'test_G.png')
    apta = Tree(); apta.G = G
    sicco_learner = Sicco_Learner(apta)
    sicco_learner.setup('test_sicco_learner_tracker.txt')
    sicco_learner.red_states = [R1, R2, R3]
    sicco_learner.blue_states = [B1, B2]
    return sicco_learner
def main():
    sicco_learner = setUp()
    sicco_learner.run_Sicco_learner()


if __name__ == '__main__':
    main()
