import cvxpy as cp
import numpy as np

# Parámetros del problema
P = np.array([[1, 0], [0, 2]])  # Matriz cuadrática (definida positiva)
q = np.array([3, 4])  # Coeficientes lineales
r = 0  # Término constante

# Restricciones
A = np.array([[1, 1]])  # Restricciones de igualdad
b = np.array([5])       # Límite de igualdad

# Variables
x = cp.Variable(2)

# Definir función objetivo
objective = cp.Minimize((1 / 2) * cp.quad_form(x, P) + q @ x + r)

# Restricciones
constraints = [A @ x == b, x >= 0]

# Formulación del problema
problem = cp.Problem(objective, constraints)

# Resolver el problema
optimal_value = problem.solve()

# Mostrar resultados
print("Valor óptimo de Z:", optimal_value)
print("Solución óptima (valores de x):")
print(f"x1 = {x.value[0]}")
print(f"x2 = {x.value[1]}")
