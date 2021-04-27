from clingo import Model
import numpy as np


class ProbabilityModule():
    '''
    Module that handles calculation or probabilities of models and atoms
    '''
    def __init__(self, models: [Model], translate_hr: bool):
        self.translate_hr = translate_hr
        self.stable_models = []
        self.model_weights = []
        self.model_probs = []
        self.calculate_probabilites(models)

    def calculate_probabilites(self, models):
        # If hard rules have been translated
        # find stable models of LPMLN
        # (ones with max hard rules satisfied)
        if self.translate_hr:
            min_alpha = min([m[1][0] for m in models])
        # TODO: Faster with list comprehension?
        for m in models:
            # If hard rules are not translated,
            # models already correspond to stable models in LPMLN
            if not self.translate_hr:
                self.stable_models.append(m[0])
                self.model_weights.append(m[1][0])
            elif self.translate_hr and m[1][0] == min_alpha:
                self.stable_models.append(m[0])
                self.model_weights.append(m[1][1])

        self.model_weights = np.exp(-np.array(self.model_weights))
        normalization_const = self.model_weights.sum()
        self.model_probs = self.model_weights / normalization_const

        # TODO: Unittest/Check that probabilities sum up to 1

    def print_models_and_probs(self):
        for i, m in enumerate(self.stable_models):
            prob = self.model_probs[i]
            print(f'Answer: {i+1}')
            model = [str(a) for a in m]
            print(model)
            print(f'Probability:  {prob:.2f} \n')

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
