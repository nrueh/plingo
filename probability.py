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
        self._calculate_probabilites(models)

    def _calculate_probabilites(self, models):
        # If hard rules have been translated
        # find stable models of LPMLN
        # (ones with max hard rules satisfied)
        if self.translate_hr:
            min_alpha = min([m[1][0] for m in models])

        for m in models:
            # If hard rules are not translated,
            # models already correspond to stable models in LPMLN
            if not self.translate_hr:
                self.stable_models.append(m[0])
                self.model_weights.append(m[1][0])
            elif self.translate_hr and m[1][0] == min_alpha:
                self.stable_models.append(m[0])
                self.model_weights.append(m[1][1])

        self.model_weights = np.exp(np.array(self.model_weights))
        normalization_const = self.model_weights.sum()
        self.model_probs = self.model_weights / normalization_const

        # TODO: Unittest/Check that probabilities sum up to 1
