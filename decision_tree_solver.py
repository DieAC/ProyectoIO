#decision_tree_solver.py
from sklearn.tree import DecisionTreeClassifier

class DecisionTreeSolver:
    def __init__(self):
        self.model = DecisionTreeClassifier()

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def visualize_tree(self):
        
        pass
