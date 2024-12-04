import cvxpy as cp
import numpy as np

P = np.array([[2, 0, 0, 0], 
              [0, 2, 0, 0], 
              [0, 0, 0, 0],  
              [0, 0, 0, 0]]) 


q = np.array([-4, -6, 0, 0])


x = cp.Variable(4)

restricciones = [
    x[0] + x[1] + x[2] == 2,
    x[0] + 5 * x[1] + x[3] == 5,  
    x >= 0  
]

objetivo = cp.Minimize(0.543 * cp.quad_form(x, P) + q.T @ x)


problema = cp.Problem(objetivo, restricciones)


resultado = problema.solve(solver=cp.ECOS, verbose=True, max_iters=2000, feastol=1e-7, abstol=1e-10)


valores_optimos = np.round(x.value, 10)
print("Valor óptimo de Z:", resultado)
print("Valores óptimos de las variables:", valores_optimos)
