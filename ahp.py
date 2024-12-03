#ahp.py
import numpy as np

class AHP:
    def __init__(self, comparison_matrix):
        self.comparison_matrix = comparison_matrix

    def calculate_weights(self):
        eigenvalues, eigenvectors = np.linalg.eig(self.comparison_matrix)
        max_eigenvalue = np.max(eigenvalues)
        weights = eigenvectors[:, np.argmax(eigenvalues)].real
        return weights / np.sum(weights)

    def consistency_ratio(self):
        
        pass
