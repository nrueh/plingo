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
            self.stable_models = list(range(len(self.model_probs)))

        for i in range(len(self.model_probs)):
            model_idx = self.stable_models[i]
            current_prob = self.model_probs[i]
            print(f'Probability of Answer {model_idx+1}: {current_prob:.2f}')
        print('\n')

    def get_query_probability(self, query):
        query_atoms = [
            a for m in self.stable_models for a in m if a.name in query
        ]
        query_atoms = list(set(query_atoms))
        n = len(self.stable_models)
        for q in query_atoms:
            query_probability = sum([
                self.model_probs[i] for i in range(n)
                if q in self.stable_models[i]
            ])
            print(f'{str(q)}: {query_probability:.2f}')
