import re

class Evaluation:
    def __init__(self, learned_graph, accepted_traces, rejected_traces): #learned_graph:Learner
        self.G = learned_graph.pta.G
        self.pta_obj = learned_graph.pta
        self.positive_traces = accepted_traces
        self.negative_traces = rejected_traces
        self.true_positive=0
        self.true_negative=0
        self.false_positive=0
        self.false_negative=0
        self.precision = 0
        self.recall =0
        self.specificity =0
        self.F_measure=0
        self.Accuracy=0
        self.BCR=0
        # self.split_dataset(accepted_traces, rejected_traces)

    def is_trace_in_G(self, trace): # trace is a set of strings ['a','a', 'b', 'x']
        s = self.G.initial_state
        for label in trace:
            input_key , output_key = self.split_input_output(label)
            s = self.G.get_target_state_for_label(s, input_key, output_key)
            if not s:
                return False, ""
        return True, s.type

    def split_input_output(self, label):
        match = re.search(r'\s*/\s*', label)
        if match:
            input_end = match.start()
            output_start = match.end()
            _input = label[:input_end]
            _output = label[output_start:]
            return _input, _output
        return None, None

    def evaluate(self):
        true_positive_lsit = []
        false_positive_list = []
        true_negative_list = []
        false_negative_list = []
        for trace in self.positive_traces:
            # print(trace)
            result, lastStateType = self.is_trace_in_G(trace)
            if result and (lastStateType == "accepted" or lastStateType == "unlabeled") :
                self.true_positive +=1
                true_positive_lsit.append(trace)
            else:
                self.false_negative +=1
                false_negative_list.append(trace)

        for trace in self.negative_traces:
            # print(trace)
            # result = self.is_trace_in_G(trace)
            result, lastStateType = self.is_trace_in_G(trace)
            if result and (lastStateType == "accepted" or lastStateType == "unlabeled"):
                self.false_positive += 1
                false_positive_list.append(trace)
            elif not result or lastStateType=="rejected":
                self.true_negative += 1
                true_negative_list.append(trace)

        self.calculate_metrics()
    def evaluate_2(self):
        self.G.delete_rejected_states()
        # This evaluation method consider the sink state as rejected state
        sink_states = self.G.find_sink_state()
        if sink_states:
            for sink_state in sink_states:
                sink_state.type = "rejected"

        true_positive_lsit = []
        false_positive_list = []
        true_negative_list = []
        false_negative_list = []
        # print(f'False Negative:')
        for trace in self.positive_traces:
            result, lastStateType = self.is_trace_in_G(trace)
            if result and (lastStateType == "accepted" or lastStateType == "unlabeled") :
                self.true_positive +=1
                true_positive_lsit.append(trace)
            else:
                # print(trace)
                self.false_negative +=1
                false_negative_list.append(trace)
        # print(f'False Positive:')
        for trace in self.negative_traces:
            # print(trace)
            # result = self.is_trace_in_G(trace)
            result, lastStateType = self.is_trace_in_G(trace)
            if result and (lastStateType == "accepted" or lastStateType == "unlabeled"):
                # print(trace)
                self.false_positive += 1
                false_positive_list.append(trace)
            elif not result or lastStateType=="rejected":
                self.true_negative += 1
                true_negative_list.append(trace)

        self.calculate_metrics()
    # def find_sink_state(self):
    #     states_with_selfloop_only = []
    #     all_states = self.G.get_all_states()
    #     for state in all_states:
    #         for child in self.G.get_children(state):
    #             if child != state and child.type != "rejected":
    #                 break
    #             states_with_selfloop_only.append(state)
    #     if len(states_with_selfloop_only) > 1:
    #         print("Warning: more than one sink state found!")
    #     if len(states_with_selfloop_only) == 0:
    #         return None
    #     return states_with_selfloop_only

    def calculate_metrics(self):
        if self.true_positive+self.false_positive == 0:
            self.precision = 0
            self.specificity = 0
        else:
            #presision: the accuracy of positive prediction
            self.precision = self.true_positive/(self.true_positive+self.false_positive)
            #specificity: the ability to find all negative samples
            self.specificity = self.true_negative/(self.true_negative+self.false_positive)
        if self.true_positive + self.false_negative == 0:
            self.recall = 0
        else:
            # recall (sensitivity): the ability to find all positive samples
            self.recall = self.true_positive / (self.true_positive + self.false_negative)
        if self.precision + self.recall == 0:
            self.F_measure = 0
        else:
            # F1-Score: prioritizing the "Positive" class and looking for a balance
            # between being accurate (Precision) and being thorough (Recall).
            self.F_measure = round((2 * self.precision * self.recall)/(self.precision + self.recall),1)
        self.Accuracy = round((self.true_positive + self.true_negative) / (len(self.positive_traces) + len(self.negative_traces)),1)
        #Balanced Classification Rate
        self.BCR = round(0.5 * (self.recall + self.specificity),1)

    def print_lst(self, lst):
        for item in lst:
            print(item)

    def write_evaluation_report(self, filename):
        with open(filename, 'a') as f:
            f.write('\n')
            f.write('Evaluation Report:\n')
            f.write(f'number of Positive traces: {len(self.positive_traces)}\n')
            f.write(f'number of Negative traces: {len(self.negative_traces)}\n')
            f.write(f'True Positive: {self.true_positive}\n')
            f.write(f'True Negative: {self.true_negative}\n')
            f.write(f'False Positive: {self.false_positive}\n')
            f.write(f'False Negative: {self.false_negative}\n')
            f.write(f'Precision: {self.precision:.2f}\n')
            f.write(f'Recall: {self.recall:.2f}\n')
            f.write(f'Specificity: {self.specificity:.2f}\n')
            f.write(f'F-measure: {self.F_measure:.2f}\n')
            f.write(f'Accuracy: {self.Accuracy:.2f}\n')
            f.write(f'BCR: {self.BCR:.2f}\n')
