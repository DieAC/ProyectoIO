import cvxpy as cp
import numpy as np

# Número de variables
num_variables = 2

# Coeficientes de la función objetivo
lineales = [3.0, 4.0]
cuadraticos = [1.0, 2.0]

# Restricciones
restricciones = [[1.0, 1.0]]  # x1 + x2 <= 5
constantes = [5.0]

# Variables de decisión
variables = [cp.Variable() for _ in range(num_variables)]

# Construir la función objetivo (minimización)
funcion_objetivo = sum(lineales[i] * variables[i] for i in range(num_variables)) + \
                   sum(cuadraticos[i] * variables[i]**2 for i in range(num_variables))

# Definir el problema objetivo
objetivo = cp.Minimize(funcion_objetivo)

# Crear las restricciones
restricciones_cp = [
    sum(restricciones[0][i] * variables[i] for i in range(num_variables)) <= constantes[0]
] + [var >= 0 for var in variables]  # Asegurarse de que las variables sean no negativas

# Resolver el problema usando el solver SCS o ECOS
problema = cp.Problem(objetivo, restricciones_cp)
resultado = problema.solve(solver=cp.ECOS, max_iters=1000, eps=1e-6)


# Imprimir resultados
print(f"Resultado: {resultado}")
print(f"Solución: {[var.value for var in variables]}")
