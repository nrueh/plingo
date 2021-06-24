import numpy as np


class ProbabilityModule():
    '''
    Module that handles calculation of probabilities of models and query atoms
    '''
    def __init__(self, model_costs, priorities, options):
        # TODO: Do weights need to be saved?
        self.translate_hr = options[0].flag
        self.two_solve_calls = options[1].flag
        self.priorities = priorities
        self.stable_models = []
        self.model_weights = []
        self.model_probs = []
        self.calculate_probabilites(np.array(model_costs))

    def calculate_probabilites(self, model_costs):
        # If hard rules have been translated
        # find stable models of LPMLN
        # (ones with max hard rules satisfied)
        model_costs = np.array(model_costs) * 10**(-5)
        self.model_weights = np.exp(-(model_costs))
        if self.two_solve_calls:
            self.model_weights = self.model_weights[:, -1]
        elif self.translate_hr and self.priorities != [0]:
            hard_weights = model_costs[:, 0]
            min_alpha = hard_weights.min()
            self.model_weights = self.model_weights[:, -1]
            self.model_weights[hard_weights != min_alpha] = 0

        self.model_weights = self.model_weights.flatten()
        self.stable_models = np.where(self.model_weights != 0)[0]
        normalization_const = self.model_weights.sum()
        self.model_probs = self.model_weights / normalization_const
        # TODO: Unittest/Check that probabilities sum up to 1

    def print_probs(self):
        print('\n')
        for s in self.stable_models:
            current_prob = self.model_probs[s]
            if current_prob < 0.000001:
                continue
            print(f'Probability of Answer {s+1}: {current_prob:.5f}')
        # TODO: Cutoff probabilities?
        print('\n')

    def get_query_probability(self, query):
        print('\n')
        for q in query:
            prob = self.model_probs[q[1]].sum()
            print(f'{str(q[0])}: {prob:.2f}')
        print('\n')
