from scipy.optimize import minimize

def objetivo(vars):
    x1, x2 = vars
    return -(x1 + x2**4) 

def restriccion1(vars):
    x1, x2 = vars
    return 9 - (3 * x1 + 2 * x2**2)


restricciones = [{'type': 'ineq', 'fun': restriccion1}]
limites = [(0, None), (0, None)] 


punto_inicial = [0.1, 2.0]

resultado = minimize(objetivo, punto_inicial, bounds=limites, constraints=restricciones, method='SLSQP')

x1, x2 = resultado.x
print("Solución óptima:")
print(f"x1 = {x1:.4f}")
print(f"x2 = {x2:.4f}")
print(f"z = {-resultado.fun:.4f}") 
