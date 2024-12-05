import tkinter as tk
from tkinter import messagebox
from scipy.optimize import minimize
import numpy as np

class ProgramacionNoConvexaVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Programación No Convexa")
        self.geometry("700x500")

        tk.Label(self, text="Ingrese la función objetivo ").pack(pady=10)
        self.func_objetivo_entry = tk.Entry(self, width=50)
        self.func_objetivo_entry.pack(pady=5)

        tk.Label(self, text="Ingrese los límites inferiores y superiores ").pack(pady=10)
        self.limites_entry = tk.Entry(self, width=20)
        self.limites_entry.pack(pady=5)

        tk.Label(self, text="Ingrese el valor inicial o iteracion ").pack(pady=10)
        self.valor_inicial_entry = tk.Entry(self, width=20)
        self.valor_inicial_entry.pack(pady=5)

        tk.Button(self, text="Resolver", command=self.resolver).pack(pady=20)

    def resolver(self):
        try:
     
            funcion_objetivo = self.func_objetivo_entry.get()
            limites_texto = self.limites_entry.get()
            valor_inicial_texto = self.valor_inicial_entry.get()

            if not funcion_objetivo or not limites_texto or not valor_inicial_texto:
                raise ValueError("Todos los campos deben estar llenos.")

            limites = list(map(float, limites_texto.split(',')))
            if len(limites) != 2 or limites[0] >= limites[1]:
                raise ValueError("Los límites deben ser dos valores separados por coma  y el primero debe ser menor que el segundo.")

            valor_inicial = [float(valor_inicial_texto)]

           
            def funcion(x):
                return eval(funcion_objetivo)

            
            resultado = minimize(funcion, valor_inicial, bounds=[(limites[0], limites[1])])

            if resultado.success:
                solucion = resultado.x[0]
                valor_objetivo = resultado.fun
                messagebox.showinfo("Resultado", f"Valor óptimo para x: {solucion}\nValor objetivo óptimo: {valor_objetivo}")
            else:
                messagebox.showerror("Error", "No se encontró una solución óptima.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver el problema: {e}")



if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  
    ventana = ProgramacionNoConvexaVentana(root)
    root.mainloop()