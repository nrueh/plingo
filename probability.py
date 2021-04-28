import numpy as np


class ProbabilityModule():
    '''
    Module that handles calculation of probabilities of models and query atoms
    '''

    # TODO: Possible to provide evidence
    def __init__(self, model_costs, translate_hr: bool):
        self.translate_hr = translate_hr
        self.stable_models = []
        self.model_weights = []
        self.model_probs = []
        self.calculate_probabilites(np.array(model_costs))

    def calculate_probabilites(self, model_costs):
        # If hard rules have been translated
        # find stable models of LPMLN
        # (ones with max hard rules satisfied)
        if self.translate_hr:
            hard_weights = model_costs[:, 0]
            self.stable_models = np.where(
                hard_weights == hard_weights.min())[0]
            model_costs = model_costs[:, 1][self.stable_models]
        model_costs = model_costs.flatten()

        self.model_weights = np.exp(-(model_costs))
        normalization_const = self.model_weights.sum()
        self.model_probs = self.model_weights / normalization_const
        # TODO: Unittest/Check that probabilities sum up to 1

    def print_probs(self):
        print('\n')
        if self.stable_models == []:
            self.stable_models = np.arange((len(self.model_probs)))

        for i in range(len(self.model_probs)):
            model_idx = self.stable_models[i]
            current_prob = self.model_probs[i]
            print(f'Probability of Answer {model_idx+1}: {current_prob:.2f}')
        print('\n')

    def get_query_probability(self, query):
        for k in query.keys():
            current_query = query[k]
            query_atoms = list(set([a[0] for a in current_query]))
            for q in query_atoms:
                model_indices = [int(t[1]) for t in current_query if t[0] == q]
                prob = self.model_probs[model_indices].sum()
                print(f'{q}: {prob:.2f}')
