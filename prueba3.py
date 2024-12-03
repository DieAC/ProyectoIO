import cvxpy as cp
import numpy as np

# Definir variables de decisión
x = cp.Variable(2)

# Definir la matriz P (coeficientes cuadráticos), el vector q (coeficientes lineales)
P = np.array([[2, 0], [0, 2]])  # Matriz de coeficientes cuadráticos (simétrica)
q = np.array([4, 3])            # Vector de coeficientes lineales

# Función objetivo (cuadrática)
objetivo = cp.Minimize(0.5 * cp.quad_form(x, P) - q.T @ x)

# Definir restricciones
restricciones = [
    x[0] + x[1] >= 3,  # Restricción 1
    x[0] - x[1] <= 1,  # Restricción 2
    x[0] >= 0,          # Restricción 3 (no negativo)
    x[1] >= 0           # Restricción 4 (no negativo)
]

# Resolver el problema
problema = cp.Problem(objetivo, restricciones)
resultado = problema.solve()

# Mostrar resultados
if resultado is not None:
    print("Valor óptimo de Z:", resultado)
    print("Solución óptima (valores de x):")
    print(f"x[0] = {x.value[0]}")
    print(f"x[1] = {x.value[1]}")
else:
    print("No se pudo encontrar una solución óptima.")
